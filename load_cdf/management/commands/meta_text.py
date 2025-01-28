
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.models import Q
# from load_cdf.models import Experiment, ExperimentAttribute, ExperimentAttributeValue,\
# Variable, VariableAttribute, VariableAttributeValue
from load_cdf.models import Experiment, ExperimentAttribute, ExperimentAttributeValue,\
Variable, VariableAttribute, VariableAttributeValue
import datetime as dt
from spacepy import pycdf
import os
from solarterra.utils import normalize_str
import random

EXPS = ['WI_OR_PRE+', 'WI_K0_SWE+', 'SPR_H1_BMSW', 'SPR_K0_BMSW', 'SPR_OR_DEF']

TO_FIND = ['Title', 'Project', 'Discipline', 'Source_name', 'Descriptor', 'Data_type', 'Data_version','Instrument_type', 'Logical_source', 'Logical_source_description', 'Mission_group', 'PI_name', 'PI_affiliation', 'Text']

class Command(BaseCommand):

    def handle(self, *args, **options):

        qfilter = Q(
            *[Q(title__iexact=item) for item in TO_FIND],
            _connector=Q.OR
        )

        exps = Experiment.objects.filter(technical_title__in=EXPS)
        for exp in exps:
            exp_attrs = exp.attributes.all()
            to_print = exp_attrs.filter( qfilter )
            for item in TO_FIND:
                one = to_print.filter(title__iexact=item).first()
                if one:
                    print(f"{item}:\t\t\t\t\t\t {one.values.first().value}")
                else:
                    print(f"{item}: ")
            
            print("Список переменных:")
            vars = exp.variables.all()
            for var in vars:
                varattrs = var.attributes.all()
                var_type = varattrs.filter(title='VAR_TYPE').first()
                if var_type.values.first().value == 'data':
                    catdesc = varattrs.filter(title='CATDESC').first()
                    field = varattrs.filter(title='FIELDNAM').first()
                    units = varattrs.filter(title='UNITS').first()
                
                    print(f"\t{field.values.first().value if field else ''} ({units.values.first().value if units else ''}) \t\t\t {catdesc.values.first().value if catdesc else ''}")
                
                    

            print("\n")