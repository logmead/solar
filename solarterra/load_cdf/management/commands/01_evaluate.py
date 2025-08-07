from django.core.management.base import BaseCommand, CommandError, CommandParser
# from load_cdf.models import dataset, datasetAttribute, datasetAttributeValue,\
# Variable, VariableAttribute, VariableAttributeValue
from load_cdf.models import Upload, CDFFileStored, Dataset, \
    Variable, VariableAttribute, VariableAttributeValue, VariableDataNRV, make_log_entry
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


# NO MANUAL INTERFERENCE IN THERE
DATA_ROOT = "/spool/data"
MATCH_FILE_DIR = "/spool/match_files"
UPLOAD_ZIP_DIR = "/spool/upload_zipped"


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

        zip_path = options["zip_path"][0]
        match_file_path = options["match_file_path"][0]

        # Check if the zip file and match file exist
        # ((❗ оно вроде бы проверяется в .sh скрипте, но на всякий случай? еще можно sys.exit использовать))
        if not os.path.isfile(zip_path):
            # log! 📃
            exit(1)

        if not os.path.isfile(match_file_path):
            # log! 📃
            exit(1)

        # --------------FILESYSTEM WORK-----------------#

        zip_md5 = subprocess.run(
            ['md5sum', zip_path], capture_output=True, text=True, check=True).stdout.split()[0]

        # Extract dataset tag from the filename
        zip_filename = os.path.basename(zip_path)
        dataset_tag, upload_human_tag = zip_filename.split(
            '_u')  # Extract part before '_u'
        upload_human_tag = upload_human_tag.rstrip(
            '.zip')  # Remove the '.zip' extension

        # Check if the dataset_tag is valid
        # ❓ проверить что ли что там пять кусочков хотя бы?

        # Create an Upload instance
        upload = Upload(
            created=dt.datetime.now(),
            human_tag=upload_human_tag,
            zip_path=zip_path,
            # zip_md5=zip_md5
        )
        upload.save()

        # 2️⃣ unarchive zip, check if file names already exist and put .cdf files where they belong

        # Create necessary directories in DATA_ROOT if they don't exist
        # if they do exist, we should check cdf file names for collisions

        dataset_dir = os.path.join(DATA_ROOT, dataset_tag.replace('_', '/'))

        # Create a temporary directory to extract the zip
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as upzip:
                upzip.extractall(temp_dir)

            # Get all CDF files from the extracted directory
            cdf_files = [f for f in os.listdir(temp_dir) if f.endswith('.cdf')]

            if not os.path.exists(dataset_dir):
                os.makedirs(dataset_dir)
                # 🚧 а если Upload валится, то удалять потом чистильщиком (будет удалять аплоаду зип и проверять пустые ли папки по тэгу датасета)
            else:
                # Check for file name collisions
                collisions = []
                for cdf_file in cdf_files:
                    target_path = os.path.join(dataset_dir, cdf_file)

                    if os.path.exists(target_path):
                        collisions.append(cdf_file)

                # If collisions found, log and exit with error code 1
                if collisions:
                    collision_list = ", ".join(collisions)
                    # log! 📃
                    upload.result_status = 2  # collision error code
                    upload.save()
                    # 🚧 save collision list as txt (куда его блин!!)
                    # with open(os.path.join(MATCH_FILE_DIR, f"{dataset_tag}_collisions.txt"), 'w') as f:
                    # f.write(f"Collisions found for dataset {dataset_tag}:\n{collision_list}\n")
                    exit(1)

                # No collisions, move files to dataset directory and create CDFFileStored instances
                upload.file_count = len(cdf_files)
                upload.save()

                for cdf_file in cdf_files:
                    target_path = os.path.join(dataset_dir, filename)

                    # Copy the file to the target directory
                    shutil.copy2(os.path.join(temp_dir, cdf_file), target_path)

                    # Create CDFFileStored instance for the file
                    cdf_stored = CDFFileStored(
                        full_path=target_path,
                        upload=upload
                    )
                    cdf_stored.save()
                    # log! 📃

        # create dataset instance if it doesnt exist and link it to upload
        dataset = Dataset.objects.get_or_none(tag=dataset_tag)
        if not dataset:
            # Create a new dataset if it doesn't exist
            dataset = Dataset(dataset_tag=dataset_tag)
            dataset.save()
        upload.dataset = dataset
        upload.save()

        # open json and save to Dataset all info from GlobalAttributes

        # Read the match file
        try:
            with open(match_file_path, 'r') as f:
                match_data = json.load(f)

            global_attrs = match_data['GlobalAttributes']

            # Mapping from JSON keys to Dataset model fields (TEXT_DESCRIPTION is missing as it requires special handling)
            dataset_field_mapping = {
                'MISSION': 'mission',
                'SOURCE_NAME': 'source_name',
                'DATA_TYPE': 'data_type',
                'INSTRUMENT': 'instrument',
                'DATASET_VERSION': 'dataset_version',
                'LOGICAL_SOURCE': 'logical_source',
                'LOGICAL_DESCRIPTION': 'logical_description',
                'PI_NAME': 'pi_name',
                'PI_AFFILIATION': 'pi_affiliation'
            }

            # Automatically populate dataset fields from JSON
            for json_key, model_field in dataset_field_mapping.items():
                if json_key in global_attrs:
                    value = global_attrs[json_key]['value']
                    setattr(dataset, model_field, value)

            # Handle text_description separately since it's a list in JSON
            if 'TEXT_DESCRIPTION' in global_attrs:
                text_list = global_attrs['TEXT_DESCRIPTION']['value']
                if isinstance(text_list, list):
                    dataset.text_description = '\n'.join(text_list)
                else:
                    dataset.text_description = str(text_list)

            dataset.save()

            # Loop through global attributes and save them to the dataset
            for attr_name, attr_value in global_attrs.items():
                dataset_attr = dataset.datasetattribute_set.get_or_create(
                    name=normalize_str(attr_name)
                )[0]

                # Create attribute value
                attr_value_obj = dataset.datasetattributevalue_set.create(
                    attribute=dataset_attr,
                    value=str(attr_value).strip(),
                    data_type=type(attr_value).__name__
                )

            # Update upload status
            upload.save()

            # Log successful processing of match file
            # make_log_entry(
            # "INFO", f"Match file {os.path.basename(match_file_path)} processed successfully")

        except json.JSONDecodeError:

            # make_log_entry(
            #     "ERROR", f"Error decoding JSON from match file: JSONDecodeError")
            upload.result_status = 3  # Match file error code
            upload.save()
            exit(3)

        except Exception as e:

            # make_log_entry("ERROR", f"Error processing match file: {str(e)}")
            upload.result_status = 3  # Match file error code
            upload.save()
            exit(3)

        # GUTTING CDF FILES for metadata extraction (not everything is stored in match file)

        # open and gut one random .cdf file
        # should be created instances of DatasetAttribute, DatasetAttributeValue,  Variable, VariableAttribute, VariableAttributeValue

        # get everything from any one file
        '''
        random_index = random.randint(0, len(files_list))

        cdf_obj = pycdf.CDF(files_list[random_index])

        for xkey, xvalue in cdf_obj.attrs.items():
            load.add_exp_attr(title=normalize_str(xkey),
                              value=str(xvalue).strip())

        for key in cdf_obj.keys():

            type_class = cdf_obj[key].dtype.__name__ if hasattr(
                cdf_obj[key].dtype, '__name__') else cdf_obj[key].dtype.__class__.__name__

            var_instance = load.add_vars(
                name=normalize_str(key),
                data_type=type_class,
                shape=str(cdf_obj[key].shape),
                nrv=not (cdf_obj[key].rv())
            )

            for attr_key, attr_value in cdf_obj[key].attrs.items():
                if attr_key == 'VAR_TYPE' and attr_value == 'data':
                    var_instance.is_data = True
                    # print(f"FOUND COMBO on {var_instance}")

                data_type = type(attr_value).__name__
                load.add_var_attr(variable=var_instance, title=normalize_str(
                    attr_key), data_type=data_type, value=str(attr_value).strip())

            if var_instance.non_record_variant:
                val_array = cdf_obj[key]
                for index, val in enumerate(val_array):
                    load.add_nrv_values(
                        variable=var_instance, value=val, order=index)

        load.dataset.save()
        load.set_unique_attr_values()
        DatasetAttribute.objects.bulk_create(load.dset_attrs)
        DatasetAttributeValue.objects.bulk_create(load.dset_attr_values)
        Variable.objects.bulk_create(load.vars)
        VariableAttribute.objects.bulk_create(load.var_attrs)
        VariableAttributeValue.objects.bulk_create(load.var_attr_values)
        VariableDataNRV.objects.bulk_create(load.nrv_data)
        make_log_entry(
            "CREATED", f"Metadata for Data Type \"{dataset_technical}\" saved")
        make_log_entry("PREPROCESSING", "Evaluation stage compeleted")

        del cdf_obj
        del load

        # result of evaluate is filled in instances of Dataset .. VariableAttribute
        '''
