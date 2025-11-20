# GUTTING CDF FILES for metadata extraction (not everything is stored in match file)

# open and gut one random .cdf file
# should be created instances of DatasetAttribute, DatasetAttributeValue,  Variable, VariableAttribute, VariableAttributeValue

# result of collect_metadata is filled in instances of Dataset .. VariableAttribute

from spacepy import pycdf
from django.core.management.base import BaseCommand, CommandError, CommandParser
from load_cdf.models import Upload, CDFFileStored, Dataset, make_log_entry, \
    DatasetAttribute, DatasetAttributeValue, Variable, VariableAttribute, VariableAttributeValue
import datetime as dt
import json
import random


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):

        # q: how can i pass a result of a python script to bash script it was launched from
        # a
