from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.core import management
from django.utils import autoreload

from load_cdf.models import *
from solarterra.utils import safe_str
from load_cdf.utils import MODEL_POSTFIX, get_django_type



def get_field_values(variable, field_title):
    field = {}
    field['title'] = safe_str(field_title)
    field_type, additions = get_django_type(variable.data_type)
    field['django_type'] = field_type
    field = field | additions
    return field
    

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("dset_title", nargs="+", type=str)

    def handle(self, *args, **options):

        dset_title = options["dset_title"][0]
        make_log_entry("START", f"Model creation script launched with parameter \"{dset_title}\"")
        
        exp = Experiment.objects.get_or_none(technical_title=exp_title)
        if exp is None:
            make_log_entry("NOT FOUND", f"Metadata for Data Type \"{dset_title}\" is not found. Please, load metadata first.")
            make_log_entry("EXIT", "Model creation script finished")
            return 0
        
        make_log_entry("FOUND", f"Metadata for the Data Type \"{dset_title}\" is found in the database")
        make_log_entry("", "Constructing model file...")

        base_name = safe_str(dset.technical_title)
        model_file_name = base_name + ".py"
        
        model_file_path = os.path.join(settings.MODEL_DIR_PATH, model_file_name)
        model_dict = m = {
            'name' : f"{base_name.upper()}{MODEL_POSTFIX}",
            'fields' : [],
        }

        dynamic_model_instance = dmi = DynamicModel(
            model_name=model_dict['name'],
            dataset_instance=dset,
            model_file_path=model_file_path
        )

        dynamic_field_list = dfl = []

        variables = dset.variables.all()
        for variable in variables:
            
            if not variable.non_record_variant:
                # check field dimensions
                if variable.data_dimensions() > 1:
                    nrv_dependency = variable.dependency_nrv_var()
                    if nrv_dependency and nrv_dependency.nrv_values.count() > 1:
                        nrvs = nrv_dependency.nrv_in_order()
                        for nrv in nrvs:
                            combined_title = f"{variable.name}_{nrv.value}"
                            field = get_field_values(variable, combined_title)
                            m['fields'].append(field)
                            dfl.append(DynamicField(
                                field_name=field['title'],
                                exploded=True,
                                variable_instance=variable,
                                dynamic_model=dmi,
                                nrv_instance=nrv,
                            ))
                            
                else:
                    field = get_field_values(variable, variable.name)
                    m['fields'].append(field)
                    dfl.append(DynamicField(
                        field_name=field['title'],
                        exploded=False,
                        variable_instance=variable,
                        dynamic_model=dmi,
                    ))

        
        content = render_to_string('model.tpl', model_dict)
        with open(model_file_path, 'w') as  model_file:
            model_file.write(content)

        make_log_entry("CREATED", f"Saved model file \"{model_file_path}\" for Data Type \"{dset_title}\"")
        
        dynamic_model_instance.save()
        DynamicField.objects.bulk_create(dynamic_field_list)
        make_log_entry("CREATED", f"Saved entry for the model \"{dmi.model_name}\"")

        make_log_entry("PREPROCESSING", "Model creation stage completed")

        
        