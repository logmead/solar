from django.core.management.base import BaseCommand
from django.core import management
from django.core.management.commands import makemigrations, migrate
from load_cdf.models import Experiment, make_log_entry
import os


"""
order of actions:

    find experiment
    find migrations file
    delete migration file
    makemigrations & migrate
    delete experiment model object

"""


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("exp_title", nargs="+", type=str)

    def handle(self, *args, **options):

        exp_title = options["exp_title"][0]
        make_log_entry("START", f"Deletion script launched with parameter \"{exp_title}\"")
        
        exp = Experiment.objects.get_or_none(technical_title=exp_title)
        if exp is None:
            make_log_entry("NOT FOUND", f"Data Type \"{exp_title}\" is not found in the database")
            make_log_entry("EXIT", "Deletion script finished")
            return 0
        else:
            make_log_entry("FOUND", f"Data Type \"{exp_title}\" is found in the database")

        
        if not hasattr(exp, 'dynamic'):
            make_log_entry("NOT FOUND", f"No model for the Data Type \"{exp_title}\"")
            exp.delete()
            make_log_entry("DELETED", f"Removed metadata for the Data Type \"{exp_title}\"")
            make_log_entry("EXIT", "Deletion script finished")
            return 0


        mod = exp.dynamic
        make_log_entry("FOUND", f"Model for the Data Type \"{exp_title}\" exists")

        if not os.path.isfile(mod.model_file_path):
            make_log_entry("NOT FOUND", f"Model file for the Data Type \"{exp_title}\" is not found")
            exp.delete()
            make_log_entry("DELETED", f"Removed metadata for the Data Type \"{exp_title}\"")
            make_log_entry("EXIT", "Deletion script finished")
            return 0

        
        make_log_entry("FOUND", f"Model file for the Data Type \"{exp_title}\" exists")

        os.remove(mod.model_file_path)
        make_log_entry("DELETED", f"Removed model file for the Data Type \"{exp_title}\"")

        exp.delete()
        make_log_entry("DELETED", f"Removed metadata for the Data Type \"{exp_title}\"")
        make_log_entry("EXIT", "Deletion script finished")
        return 0

        

