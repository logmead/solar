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
    leng = 0
    for field in dynamic_fields:
        var = field.variable_instance

        # get part of values if varaible is multidimensional
        if field.exploded:
            array = cdf_object[var.name][:, field.exploded_index]
        else:
            array = cdf_object[var.name][...]    
        
        if len(array) > leng:
            leng = len(array)
       
        print(field.field_name, len(array))

        # if array of timestamps
        if var.datatype == 'CDF_EPOCH':
            #val_min, val_min_type = var.get_attribute_value("validmin", get_type=True)
            #vin = make_type(val_min, val_min_type)
            #val_max, val_max_type = var.get_attribute_value("validmax", get_type=True)
            #vax = make_type(val_max, val_max_type)
            
            #arrays[field.field_name] = list(map(lambda x: ts_bigint_resolver(x) if x > vin and x < vax else None, array))
            arrays[field.field_name] = list(map(lambda x: ts_bigint_resolver(x), array))
        else: 
            arrays[field.field_name] = array
            
        # if array of floats
        """
        elif var.is_decimal():
            print(f"var {var} is decimal")
            # print(f"NEW ARRAY {array.dtype}, {type(array)}")
            
            places, digits = var.get_precision()
            fill_val = var.fillval

            b = array.astype(str)

            b[b == fill_val] = math.nan
            str_nan = str(math.nan)
            context = Context(prec=digits)
            setcontext(context)

            places = Decimal(str(10 ** -(places)))            
            ll = []
            for index, x in enumerate(b):
                if x == str_nan:
                    ll.append(None)
                else:
                    #try:
                    print(x, places, digits)
                    item = Decimal(x).quantize(places, context=context)
                    ll.append(item)
                    #except Exception as e:
                    #    ll.append(None)
                    #    print("ERRROR IN FLOAT")
                    #    print(index, f"|{x}|")
                    #    print(e)
                    #    exit()

            arrays[field.field_name] = ll
            #arrays[field.field_name] = list(map(lambda x: None if x == str_nan else Decimal(x).quantize(places, context=context), b))
        """
            
        # any other array
            
        #fill_val, fill_val_type = var.get_attribute_value("fillval", get_type=True)
        #fill = make_type(fill_val, fill_val_type)
        #arrays[field.field_name] = list(map(lambda x: None if x == fill else x, array))
        
    return leng, arrays
            
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("dataset_tag", nargs="+", type=str)

    def handle(self, *args, **options):

        dataset_tag = options["dataset_tag"][0]
        
        # find experiment
        dataset_instance = Dataset.objects.get_or_none(tag=dataset_tag)
        if dataset_instance is None:
            print(f"{dataset_instance} dataset not found")
            #make_log_entry("NOT FOUND", f"Metadata for Data Type \"{exp_title}\" is not found. Please, load metadata first.")
            #make_log_entry("EXIT", "Data loading script finished")
            return 0
        
        #make_log_entry("FOUND", f"Metadata for the Data Type \"{exp_title}\" is found in the database")
        

        # find model
        if hasattr(dataset_instance, 'dynamic'):
            dynamic_model_instance = dmi = dataset_instance.dynamic
        else:
            print("dynamic model not found")
            #make_log_entry("NOT FOUND", f"No model for the Data Type \"{exp_title}\".Please, create the model first.")
            #make_log_entry("EXIT", "Data loading script finished")
            return 0


        if dmi is not None:
            model_class = dmi.resolve_class()
            if model_class is None:
                print("model class not found")
                #make_log_entry("NOT FOUND", f"No model for the Data Type \"{exp_title}\".Please, create the model first.")
                #make_log_entry("EXIT", "Data loading script finished")
                return 0
        
        print("model", model_class)
        
        #make_log_entry("FOUND", f"Model for the Data Type \"{exp_title}\" exists")

        files_list = []
        for (dirpath, dirnames, filenames) in os.walk(dataset_instance.directory):
            files_list.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.cdf')])
        
        file_number = len(files_list)
        print('file_number', file_number)
        #make_log_entry("FOUND", f"In \"{exp.dir_path}\" found \"{file_number}\" .cdf files")

        if file_number == 0:
            print("no files found")
            make_log_entry("EXIT", "Data loading script finished")
            return 0
        
        
        #variables = exp.variables.all()
        #any_rv = variables.filter(non_record_variant=False).first()
        dynamic_fields = dmi.fields.all()
        #make_log_entry("", "Starting data parsing...")

        counter = 0
        
        for file_path in files_list:
            
            file_name = file_path.strip('/').split('/')[-1]
            print("FILE", file_name) 
            cdf_object = pycdf.CDF(file_path)

            #model_instances = [model_class() for _ in range(leng)]
            

            # get all value arrays in a dict with keys
            leng, field_dict = value_arrays(dynamic_fields, cdf_object)
            
            model_instances = []

            # set data
            for index in range(leng):

                instance = model_class()
                setattr(instance, 'file_name', file_name)

                for attr, vals in field_dict.items():
                    if index < len(vals):
                        setattr(instance, attr, vals[index])

                model_instances.append(instance)

            #model_instances[:] = [inst for inst in model_instances if inst.epoch is not None]            
            
            
            del cdf_object
            del field_dict    
            
            
            try:
                model_class.objects.bulk_create(model_instances)
            except Exception as e:
                print(e)
                print(repr(e))
                exit()
                #make_log_entry("ERROR", f"Could not load data from {file_name}. Exception {e.__class__.__name__} occured.", addition=e)
            else:
                counter += 1

            #make_log_entry("CREATED", f"Loaded {len(model_instances)} entries from {file_name}")
            
            del model_instances
            #if counter % 10 == 0:
            #    make_log_entry("CREATED", f"Loaded {counter} files...")
        
        #make_log_entry("CREATED", f"Loaded {counter} files out of {len(files_list)}.")
        #make_log_entry("EXIT", "Data loading script finished")
        


