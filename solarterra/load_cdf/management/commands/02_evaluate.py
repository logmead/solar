from django.core.management.base import BaseCommand, CommandError, CommandParser
# from load_cdf.models import dataset, datasetAttribute, datasetAttributeValue,\
# Variable, VariableAttribute, VariableAttributeValue
from load_cdf.models import Upload, CDFFileStored, Dataset, DatasetAttribute, DatasetAttributeValue, \
    Variable, VariableAttribute, VariableAttributeValue, make_log_entry
import datetime as dt
from spacepy import pycdf
import os
import tempfile
import shutil
import zipfile
import random
import subprocess
import json
from solarterra.utils import normalize_str
from django.conf import settings

# NO MANUAL INTERFERENCE IN THERE
DATA_ROOT = "/spool/data"
MATCH_FILE_DIR = "/spool/match_files"
UPLOAD_ZIP_DIR = "/spool/uploads_zipped"


def get_var_field(mf_str):
    if mf_str.startswith('MF_'):
        return mf_str[3:].lower()
    elif mf_str.startswith('MFLBL_'):
        return mf_str[6:].lower()
    else:
        print(f"JSON: VAR ATTRIBUTE NAME is weird {mf_str}")


class MetaAggregator():
    def __init__(self, upload, dataset):
        # TODO: maybe i want utag and dtag instead of instances?
        self.upload = upload
        self.dataset = self.upload.dataset

        self.dset_attrs = []

        self.dset_attr_values = []

        self.vars = []

        self.var_attrs = []

        self.var_attr_values = []

        # self.nrv_data = []


class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser is a built-in BaseCommand class that takes command line arguments
        # narg is a number of arguments that can be passed to the command
        # nargs can be a number, a + or a *, where + means one or more
        # if nargs is present, options will be a list of arguments, even if nargs = 1
        parser.add_argument("zip_path", nargs=1, type=str)
        parser.add_argument("match_file_path", nargs=1, type=str)

    def handle(self, *args, **options):

        # INPUT
        """
        FILE_HIERARCHY == DATASET_TAG
        INPUT FOR THE COMMAND: [FILE_HIERARCHY]_u[..] (WIND_WIND_OR_PRE_v01_u1)
            [FILE_HIERARCHY]_u[..].json match file in /spool/match_files
            [FILE_HIERARCHY]_u[..].zip containing cdf files of this dataset in /spool/dataset_zipped

        """

        zip_path = os.path.join(UPLOAD_ZIP_DIR, options["zip_path"][0])
        print(f"zip_path: {zip_path}")
        zip_filename = os.path.basename(zip_path)
        match_file_path = os.path.join(
            MATCH_FILE_DIR, options["match_file_path"][0])
        print(f"match_file_path: {match_file_path}")
        match_file_name = os.path.basename(match_file_path)

        # Check if the zip file and match file exist
        # ((❗ оно вроде бы проверяется в .sh скрипте, но на всякий случай? еще можно sys.exit использовать))
        if not os.path.isfile(zip_path):
            exit(1)

        if not os.path.isfile(match_file_path):
            exit(1)

        # --------------FILESYSTEM WORK-----------------#

        # zip_md5 = subprocess.run(
        #     ['md5sum', zip_path], capture_output=True, text=True, check=True).stdout.split()[0]

        # Extract dataset tag from the filename

        dataset_tag, upload_u_tag = zip_filename.split(
            '_u')  # Extract part before '_u'
        upload_u_tag = upload_u_tag.rstrip(
            '.zip')  # Remove the '.zip' extension

        # Check if the dataset_tag is valid
        # ❓ проверить что ли что там пять кусочков хотя бы?

        # Create an Upload instance
        upload = Upload(
            created=dt.datetime.now(),
            u_tag=upload_u_tag,
            zip_path=zip_path,
            # zip_md5=zip_md5
        )

        upload.save()

        # Log the upload creation
        make_log_entry(
            "START", f"Processing upload for {zip_filename} and {match_file_name}. Target dataset is: {dataset_tag}, upload tag: {upload_u_tag}",
            upload=upload)

        # 2️⃣ unarchive zip, check if file names already exist and put .cdf files where they belong

        # Create necessary directories in DATA_ROOT if they don't exist
        # if they do exist, we should check cdf file names for collisions

        dataset_dir = os.path.join(DATA_ROOT, dataset_tag.replace('_', '/'))

        # create dataset instance if it doesnt exist and link it to upload
        dataset = Dataset.objects.get_or_none(tag=dataset_tag)
        if dataset is None:
            # Create a new dataset if it doesn't exist
            dataset = Dataset(tag=dataset_tag, directory=str(dataset_dir))
            dataset.save()
            make_log_entry(
                "CREATED", f"Dataset instance created for {dataset_tag}",
                upload=upload)
        else:
            make_log_entry(
                "FOUND EXISTING", f"Dataset instance already exists for {dataset_tag}.",
                upload=upload)
        upload.dataset = dataset
        upload.save()
        # Log the dataset creation

        # Create a temporary directory to extract the zip
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as upzip:
                upzip.extractall(temp_dir)

            # Get all CDF files from the extracted directory
            cdf_files = [f for f in os.listdir(temp_dir) if f.endswith('.cdf')]

            if not os.path.exists(dataset_dir):
                os.makedirs(dataset_dir)
                make_log_entry(
                    "CREATED", f"Created dataset directory: {dataset_dir}", upload=upload)
                # 🚧 а если Upload валится, то удалять потом чистильщиком (будет удалять аплоаду зип и проверять пустые ли папки по тэгу датасета)
            else:
                make_log_entry(
                    "FOUND EXISTING", f"Dataset directory already exists: {dataset_dir}, proceeding to detecting file collisions", upload=upload)
                # Check for file name collisions
                collisions = []
                for cdf_file in cdf_files:
                    target_path = os.path.join(dataset_dir, cdf_file)

                    if os.path.exists(target_path):
                        collisions.append(cdf_file)

                # If collisions found, log and exit with error code 1
                if collisions:
                    collision_list = "\n".join(collisions)
                    # save collision list as txt
                    collision_logs_txt = os.path.join(
                        settings.COLLISIONS_LOGS, f"{dataset_tag}_{upload.u_tag}_collisions.txt")
                    with open(collision_logs_txt, 'w') as f:
                        f.write(
                            f"Collisions found for dataset {dataset_tag}:\n{collision_list}")
                    make_log_entry(
                        "ERROR", f"Collisions found for dataset {dataset_tag}. Collisions saved in the {collision_logs_txt}",
                        upload=upload)
                    upload.result_status = 2  # collision error code
                    upload.save()
                    make_log_entry(
                        "EXIT", f"Exiting due to collisions in dataset {dataset_tag}. Check the collision logs at {collision_logs_txt}",
                        upload=upload)
                    exit(2)

            # No collisions, move files to dataset directory and create CDFFileStored instances
            make_log_entry(
                "OK", f"No collisions found for dataset {dataset_tag}, proceeding to storing files", upload=upload)
            upload.file_count = len(cdf_files)
            upload.save()

            for cdf_file in cdf_files:
                # TODO: remake it into a bulk save
                target_path = os.path.join(dataset_dir, cdf_file)

                # Copy the file to the target directory
                shutil.copy2(os.path.join(temp_dir, cdf_file), target_path)

                # Create CDFFileStored instance for the file
                cdf_stored = CDFFileStored(
                    full_path=target_path,
                    upload=upload
                )
                cdf_stored.save()
            make_log_entry(
                'OK', f"All CDF files stored successfully in {dataset_dir}", upload=upload)

        # open json and save to Dataset all info from GlobalAttributes

        # Read the match file
        try:
            with open(match_file_path, 'r') as f:
                match_data = json.load(f)
            make_log_entry(
                "OK", f"Match file {match_file_name} loaded successfully", upload=upload)

            global_attrs = match_data['GlobalAttributes']
            upload.matchfile_verision = global_attrs['MATCHFILE_VERSION']['value']

            # Mapping from JSON keys to Dataset model fields (TEXT_DESCRIPTION is missing as it requires special handling)
            # tbh maybe a list and lowercase would be better
            dataset_fields = [
                'MISSION', 'SOURCE_NAME', 'DATA_TYPE',
                'INSTRUMENT', 'DATASET_VERSION', 'LOGICAL_SOURCE',
                'LOGICAL_DESCRIPTION', 'PI_NAME', 'PI_AFFILIATION'
            ]

            # Automatically populate dataset fields from JSON
            for field in dataset_fields:
                if field in global_attrs:
                    value = global_attrs[field]['value']
                    setattr(dataset, field.lower(), value)

            # Handle text_description separately since it's a list in JSON
            if 'TEXT_DESCRIPTION' in global_attrs:
                text_list = global_attrs['TEXT_DESCRIPTION']['value']
                if isinstance(text_list, list):
                    dataset.text_description = '\n'.join(text_list)
                else:
                    dataset.text_description = str(text_list)

            dataset.save()
            make_log_entry(
                "OK", f"Dataset {dataset_tag} updated with global attributes from match file", upload=upload)
            # Update upload status
            upload.save()

            # Log successful processing of match file
            # make_log_entry(
            # "INFO", f"Match file {os.path.basename(match_file_path)} processed successfully")

        except json.JSONDecodeError:

            make_log_entry(
                "ERROR", f"Error decoding JSON from match file: JSONDecodeError. Check if the file is a valid JSON.", upload=upload)
            upload.result_status = 3  # Match file error code
            upload.save()
            make_log_entry(
                "EXIT", f"Exiting due to error processing match file", upload=upload)
            exit(3)

        except Exception as e:

            make_log_entry(
                "ERROR", f"Error processing match file: {str(e)}", upload=upload)
            upload.result_status = 3  # Match file error code
            upload.save()
            make_log_entry(
                "EXIT", f"Exiting due to error processing match file", upload=upload)
            exit(3)

        # -------UNTESTED BELOW THIS LINE-------#
        mama = MetaAggregator(upload, dataset)

        # Create reverse mappings for easy lookup
        namemap_dtsattr_reversed = {}
        for attr_name, vals in match_data['GlobalAttributes'].items():
            if "gattribute_name" in match_data['GlobalAttributes'][attr_name]:
                namemap_dtsattr_reversed[vals["gattribute_name"]] = attr_name

        namemap_vars_reversed = {}
        for var_name in match_data['Variables']:
            for varattr_name, vals in match_data['Variables'][var_name].items():
                if 'vattribute_name' in vals:
                    namemap_vars_reversed[vals['vattribute_name']] = var_name

        # dataset attribute creation
        # - choose cdf_file instance, open it
        cdf_obj = pycdf.CDF(cdf_stored.full_path)

        for xkey, xvalue in cdf_obj.attrs.items():
            da_instance = DatasetAttribute(
                title=xkey,
                dataset=dataset,
                linked_standard_field=namemap_dtsattr_reversed.get(xkey, None),
            )
            dav_instance = DatasetAttributeValue(
                value=xvalue,
                attribute=da_instance
            )
            mama.dset_attrs.append(da_instance)
            mama.dset_attr_values.append(dav_instance)

        DatasetAttribute.objects.bulk_create(mama.dset_attrs)
        DatasetAttributeValue.objects.bulk_create(mama.dset_attr_values)

        # get varibales from the CDF
        for var in cdf_obj.keys():
            var_instance = Variable(
                name=var,
                dataset=dataset
            )
            mama.vars.append(var_instance)

            for attr_title, attr_value in cdf_obj[var].attrs.items():
                var_attr_instance = VariableAttribute(
                    title=attr_title,
                    variable=var_instance
                )
                mama.var_attrs.append(var_attr_instance)

                var_attr_value_instance = VariableAttributeValue(
                    value=attr_value,
                    attribute=var_attr_instance
                )
                mama.var_attr_values.append(var_attr_value_instance)

        Variable.objects.bulk_create(mama.vars)
        VariableAttribute.objects.bulk_create(mama.var_attrs)
        VariableAttributeValue.objects.bulk_create(mama.var_attr_values)

        # updating variable, varattrs using json
        var_qs = Variable.objects.filter(dataset=dataset)

        for var_name, var_dict in match_data['Variables'].items():
            # find instance of this variable
            try:
                var_instance = var_qs.get(name=var_name)
            except Exception as e:
                print(
                    f"SASHAAAAA {var_name} variable does not exist in the cdf file")
                print(e)
                continue

            for json_var_attr, var_attr_dict in var_dict.items():
                # find Variable instance field to save data to
                var_field = get_var_field(json_var_attr)

                if var_attr_dict['value'] is None:
                    continue
                # save data
                try:
                    print(var_instance.name, var_field, var_attr_dict['value'])
                    setattr(var_instance, var_field,
                            str(var_attr_dict['value']))

                except Exception as e:
                    print(
                        f"OMG {var_instance}, {var_field}, {var_attr_dict['value']}, {type(var_attr_dict['value'])}, {e}")

                # find the var attr instance
                if var_attr_dict['vattribute_name'] is None:
                    continue
                try:
                    var_attr_instance = var_instance.attributes.get(
                        title=var_attr_dict['vattribute_name'])
                except Exception as e:
                    # print(
                    #    f"SASHAAAAA var {var_name} {var_attr_dict['vattribute_name']} var_attr does not exist in the cdf file")
                    # print(e)
                    continue
                var_attr_instance.linked_standard_field = var_field
                var_attr_instance.multipart = var_attr_dict['value'] is list
                var_attr_instance.save()

            """
            adding dimension values to explode later
            - check if variable attributes contain depend 1
            - in cdf file, fing variable from depend 1 and save 
            its value into the dim_values of the current variable
            """

            """
            notion abt depend_x attributes:
            so, variable have a match-file attributes: 
            MFLBL_DIMS и MFLBL_DIM_SIZES: first it 0 for scalars, then 1 for 1d arrays etc; second is a list of sizes for each dimention
            the initial CDF variable has a must-have field DEPEND_x, which points to another variable in the CDF file
            TODO: j: i am not completely sure if it's always present/correctly filled; 
            """
            explosion = var_instance.attributes.filter(
                title__icontains='depend_1') #TODO: it's not only depend_1: it currently supports only one dimention
            if explosion.count() > 0:
                depend_var = explosion.first().get_value()
                var_instance.dim_values = str(cdf_obj[depend_var][...])
                print(
                    f"{dataset} found explosion {var_instance} {depend_var} {var_instance.dim_values}")
            try:
                var_instance.save()
            except Exception as e:
                print(dataset, var_instance.name, e)

        # get variables that do not have matchfile var_logic_type set
        # and set it manually from the VAR_TYPE attribute
        set_var_type = var_qs.filter(var_logic_type__isnull=True)

        for var in set_var_type:
            var.var_logic_type = var.attributes.get(
                title='VAR_TYPE').get_value()
            var.save()

        # upload.result_status = 1  # Success code
        # upload.save()
        # make_log_entry(
        #     "SUCCESS", f"Upload {zip_filename} processed successfully with dataset {dataset_tag}. YAY.", upload=upload)
        # make_log_entry(
        #     "EXIT", f"test of new upload model ok!!!")
