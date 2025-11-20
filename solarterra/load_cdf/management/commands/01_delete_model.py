from django.core.management.base import BaseCommand
from django.core import management
from django.core.management.commands import makemigrations, migrate
from load_cdf.models import Dataset, make_log_entry
import os


"""
order of actions:

    find dataset
    find migrations file
    delete migration file
    makemigrations & migrate
    delete dataset model object

"""


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("dst_tag", nargs="+", type=str)

    def handle(self, *args, **options):

        dst_tag = options["dst_tag"][0]
        make_log_entry(
            "START", f"Deletion script launched with parameter \"{dst_tag}\"")

        dst = Dataset.objects.get_or_none(tag=dst_tag)
        if dst is None:
            make_log_entry(
                "NOT FOUND", f"Data Type \"{dst_tag}\" is not found in the database")
            make_log_entry("EXIT", "Deletion script finished")
            return 0
        else:
            make_log_entry(
                "FOUND", f"Data Type \"{dst_tag}\" is found in the database")

        if not hasattr(dst, 'dynamic'):
            make_log_entry(
                "NOT FOUND", f"No model for the Data Type \"{dst_tag}\"")
            dst.delete()
            make_log_entry(
                "DELETED", f"Removed metadata for the Data Type \"{dst_tag}\"")
            make_log_entry("EXIT", "Deletion script finished")
            return 0

        mod = dst.dynamic
        make_log_entry(
            "FOUND", f"Model for the Data Type \"{dst_tag}\" exists")

        if not os.path.isfile(mod.model_file_path):
            make_log_entry(
                "NOT FOUND", f"Model file for the Data Type \"{dst_tag}\" is not found")
            dst.delete()
            make_log_entry(
                "DELETED", f"Removed metadata for the Data Type \"{dst_tag}\"")
            make_log_entry("EXIT", "Deletion script finished")
            return 0

        make_log_entry(
            "FOUND", f"Model file for the Data Type \"{dst_tag}\" exists")

        os.remove(mod.model_file_path)
        make_log_entry(
            "DELETED", f"Removed model file for the Data Type \"{dst_tag}\"")

        dst.delete()
        make_log_entry(
            "DELETED", f"Removed metadata for the Data Type \"{dst_tag}\"")
        make_log_entry("EXIT", "Deletion script finished")
        return 0
