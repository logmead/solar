from django.core.management.base import BaseCommand
from django.apps import apps
import os
from load_cdf.models import *
from data_cdf.models import *
from spacepy import pycdf
from solarterra.utils import ts_bigint_resolver
from load_cdf.utils import make_type
from decimal import Decimal, Context, getcontext, setcontext
from django.core.exceptions import  ValidationError
import math



# construct value lists once per file, cause joins
def value_arrays(dynamic_fields, cdf_object):
    arrays = {}
    
    for field in dynamic_fields:
        var = field.variable_instance

        # get part of values if varaible is multidimensional
        if field.exploded:
            array = cdf_object[var.name][:, field.nrv_instance.order]
        else:
            array = cdf_object[var.name][...]    
            
        

        # if array of timestamps
        if var.is_datetime():

            val_min, val_min_type = var.get_attribute_value("validmin", get_type=True)
            vin = make_type(val_min, val_min_type)
            val_max, val_max_type = var.get_attribute_value("validmax", get_type=True)
            vax = make_type(val_max, val_max_type)
            
            arrays[field.field_name] = list(map(lambda x: ts_bigint_resolver(x) if x > vin and x < vax else None, array))
            
            
        # if array of floats
        elif var.is_decimal():
            
            # print(f"NEW ARRAY {array.dtype}, {type(array)}")
            
            places, digits = var.get_precision()
            fill_val = var.get_attribute_value("fillval")

            b = array.astype(str)

            b[b == fill_val] = math.nan
            str_nan = str(math.nan)
            context = Context(prec=digits)
            setcontext(context)

            places = Decimal(str(10 ** -(places)))


            try:
                arrays[field.field_name] = list(map(lambda x: None if x == str_nan else Decimal(x).quantize(places, context=context), b))
            except Exception as e:
                print("ERRROR IN FLOAT")
                print(e)
                exit()

            
        # any other array
        else:

            fill_val, fill_val_type = var.get_attribute_value("fillval", get_type=True)
            fill = make_type(fill_val, fill_val_type)
            arrays[field.field_name] = list(map(lambda x: None if x == fill else x, array))
            
    return arrays
            
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("exp_title", nargs="+", type=str)

    def handle(self, *args, **options):

        exp_title = options["exp_title"][0]
        make_log_entry("START", f"Data loading script launched with parameter \"{exp_title}\"")
        
        # find experiment
        exp = Experiment.objects.get_or_none(technical_title=exp_title)
        if exp is None:
            make_log_entry("NOT FOUND", f"Metadata for Data Type \"{exp_title}\" is not found. Please, load metadata first.")
            make_log_entry("EXIT", "Data loading script finished")
            return 0
        
        make_log_entry("FOUND", f"Metadata for the Data Type \"{exp_title}\" is found in the database")
        

        # find model
        if hasattr(exp, 'dynamic'):
            dynamic_model_instance = dmi = exp.dynamic
        else:
            make_log_entry("NOT FOUND", f"No model for the Data Type \"{exp_title}\".Please, create the model first.")
            make_log_entry("EXIT", "Data loading script finished")
            return 0


        if dmi is not None:
            model_class = dmi.resolve_class()
            if model_class is None:
                make_log_entry("NOT FOUND", f"No model for the Data Type \"{exp_title}\".Please, create the model first.")
                make_log_entry("EXIT", "Data loading script finished")
                return 0

        
        make_log_entry("FOUND", f"Model for the Data Type \"{exp_title}\" exists")

        files_list = []
        for (dirpath, dirnames, filenames) in os.walk(exp.dir_path):
            files_list.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.cdf')])
        
        file_number = len(files_list)
        
        make_log_entry("FOUND", f"In \"{exp.dir_path}\" found \"{file_number}\" .cdf files")

        if file_number == 0:
            make_log_entry("EXIT", "Data loading script finished")
            return 0

        
        variables = exp.variables.all()
        any_rv = variables.filter(non_record_variant=False).first()
        dynamic_fields = dmi.fields.all()
        make_log_entry("", "Starting data parsing...")

        counter = 0
        
        for file_path in files_list:
            
            file_name = file_path.strip('/').split('/')[-1]
            
            cdf_object = pycdf.CDF(file_path)
            leng = len(cdf_object[any_rv.name])
            model_instances = [model_class() for _ in range(leng)]
            

            # get all value arrays in a dict with keys
            field_dict = value_arrays(dynamic_fields, cdf_object)
            

            # set data
            for index in range(leng):
                setattr(model_instances[index], 'file_name', file_name)

                for attr, vals in field_dict.items():
                    setattr(model_instances[index], attr, vals[index])

            
            model_instances[:] = [inst for inst in model_instances if inst.epoch is not None]            
            
            
            del cdf_object
            del field_dict    
            
            
            try:
                model_class.objects.bulk_create(model_instances)
            except Exception as e:
                print(e)
                print(repr(e))
                exit()
                make_log_entry("ERROR", f"Could not load data from {file_name}. Exception {e.__class__.__name__} occured.", addition=e)
            else:
                counter += 1

            #make_log_entry("CREATED", f"Loaded {len(model_instances)} entries from {file_name}")
            
            del model_instances
            if counter % 10 == 0:
                make_log_entry("CREATED", f"Loaded {counter} files...")

        make_log_entry("CREATED", f"Loaded {counter} files out of {len(files_list)}.")
        make_log_entry("EXIT", "Data loading script finished")
            


