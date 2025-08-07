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
COLLISION_LOGS_DIR = "/spool/collision_logs"


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
        zip_filename = os.path.basename(zip_path)
        match_file_path = options["match_file_path"][0]
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

        dataset_tag, upload_ziptag = zip_filename.split(
            '_u')  # Extract part before '_u'
        upload_ziptag = upload_ziptag.rstrip(
            '.zip')  # Remove the '.zip' extension

        # Check if the dataset_tag is valid
        # ❓ проверить что ли что там пять кусочков хотя бы?

        # Create an Upload instance
        upload = Upload(
            created=dt.datetime.now(),
            ziptag=upload_ziptag,
            zip_path=zip_path,
            # zip_md5=zip_md5
        )
        upload.save()

        # Log the upload creation
        make_log_entry(
            "START", f"Processing upload for {zip_filename} and {match_file_name}. Target dataset is: {dataset_tag}, upload zip tag: {upload_ziptag}",
            upload=upload)

        # 2️⃣ unarchive zip, check if file names already exist and put .cdf files where they belong

        # Create necessary directories in DATA_ROOT if they don't exist
        # if they do exist, we should check cdf file names for collisions

        dataset_dir = os.path.join(DATA_ROOT, dataset_tag.replace('_', '/'))

        # create dataset instance if it doesnt exist and link it to upload
        dataset = Dataset.objects.get_or_none(tag=dataset_tag)
        if not dataset:
            # Create a new dataset if it doesn't exist
            dataset = Dataset(dataset_tag=dataset_tag)
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
                        COLLISION_LOGS_DIR, f"{dataset_tag}_{upload.ziptag}_collisions.txt")
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
                    target_path = os.path.join(dataset_dir, filename)

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
            upload.matchfile_verision = match_data['MATCHFILE_VERSION']['value']

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

        upload.result_status = 1  # Success code
        upload.save()
        make_log_entry(
            "SUCCESS", f"Upload {zip_filename} processed successfully with dataset {dataset_tag}. YAY.", upload=upload)
        make_log_entry(
            "EXIT", f"test of new upload model ok!!!")

        # GUTTING CDF FILES for metadata extraction (not everything is stored in match file)

        # open and gut one random .cdf file
        # should be created instances of DatasetAttribute, DatasetAttributeValue,  Variable, VariableAttribute, VariableAttributeValue

        # result of evaluate is filled in instances of Dataset .. VariableAttribute
