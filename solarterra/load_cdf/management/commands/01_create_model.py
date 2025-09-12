from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.core import management
from django.utils import autoreload

from load_cdf.models import *
from solarterra.utils import safe_str
from load_cdf.utils import MODEL_POSTFIX, get_django_type


# brun this whole file

def get_field_values(variable, postfix=None):
    field = {}
    field['title'] = safe_str(variable.name)
    if postfix is not None:
        field['title'] += f"_{postfix}"
    field['datatype'] = DataType.object.get(cdf_file_label=variable.datatype)

    return field


# REMOVE THIS FOR THE GENERAL CASE
def parse_dim_values(dim_values_str):
    raw_values = dim_values.strip('[]').split().strip('\'')
    return [item.replace('.-', '_') for item in map(lambda x: x.strip('\''), raw_values) if item != '']


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("dataset_tag", nargs="+", type=str)

    def handle(self, *args, **options):

        dataset_tag = options["dataset_tag"][0]
        print(dataset_tag)
        dataset_instance = Dataset.objects.get_or_none(tag=dataset_tag)

        if dataset_instance is None:
            print(f"did not find dataset {dataset_tag}")
            return 0

        model_file_name = dataset_tag + ".py"

        model_file_path = os.path.join(
            settings.MODEL_DIR_PATH, model_file_name)

        model_dict = m = {
            'name': f"{dataset_tag}{MODEL_POSTFIX}",
            'fields': [],
        }

        dynamic_model_instance = dmi = DynamicModel(
            model_name=model_dict['name'],
            dataset_instance=dataset_instance,
            model_file_path=model_file_path
        )

        dynamic_field_list = dfl = []

        variables = dataset_instance.variables.all()

        for variable in variables:
            if variable.dim_sizes > 1:
                # create dim_sizes model fields instead of one
                for field_postfix in parse_dim_values(variable.dim_values):
                    field = get_field_values(variable, field_postfix)
                    m['fields'].append(field)

                    dfl.append(DynamicField(
                        field_name=field['title'],
                        exploded=False,
                        variable_instance=variable,
                        dynamic_model=dmi,
                    ))
            else:
                field = get_field_values(variable)
                m['fields'].append(field)

                dfl.append(DynamicField(
                    field_name=field['title'],
                    exploded=False,
                    variable_instance=variable,
                    dynamic_model=dmi,
                ))

            """
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
            """

        content = render_to_string('model.tpl', model_dict)
        with open(model_file_path, 'w') as model_file:
            model_file.write(content)

        # make_log_entry(
        #     "CREATED", f"Saved model file \"{model_file_path}\" for Data Type \"{dset_title}\"")

        dynamic_model_instance.save()
        DynamicField.objects.bulk_create(dynamic_field_list)
        # make_log_entry(
        #     "CREATED", f"Saved entry for the model \"{dmi.model_name}\"")

        # make_log_entry("PREPROCESSING", "Model creation stage completed")
