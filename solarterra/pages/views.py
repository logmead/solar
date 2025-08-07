from django.shortcuts import render
from load_cdf.models import DynamicModel, DynamicField, Variable, LogEntry, Dataset, DatasetAttribute, VariableAttribute
from data_cdf.models import *
from django.http import Http404
from django.apps import apps
from solarterra.utils import bigint_ts_resolver
from django.db.models import Max, Min
from django.conf import settings
from django.db import connection


def main_page(request):
    template = "pages/main.html"
    context = {"main_page": True}
    return render(request, template, context)


def system_data(request):
    template = "pages/system_data.html"
    cursor = connection.cursor()
    cursor.execute('select version();')
    row = cursor.fetchone()
    context = {
        'version': settings.PROJECT_VERSION,
        'path': settings.BASE_DIR,
        'hashsum': '',
        'db_version': row[0],

    }

    return render(request, template, context)


def data_info(request):
    template = "pages/data_official.html"
    context = {
        "models": []
    }

    dynamic_models = DynamicModel.objects.order_by(
        '-dataset_instance__created')
    for dm in dynamic_models:
        model_class = dm.resolve_class()
        dts = dm.dataset_instance

        # check loading script for wi_ho consistency with times

        ts_start_limit, ts_end_limit = dm.get_time_limits()
        t_start = ts_start_limit.date() if ts_start_limit else ""
        t_end = ts_end_limit.date() if ts_end_limit else ""
        time_delta_str = f"{t_start}  -  {t_end}"

        # multidim = var.get_attribute_value('depend_1')

        vars = dm.dataset_instance.variables.filter(
            non_record_variant=False)
        var_dicts = [{
            'name': var.name,
            'description': var.get_attribute_value('fieldnam'),
            'data_type': var.is_data,
            'depends_on': var.get_attribute_value('depend_0'),
            'multidim': var.dependency_nrv_var().nrv_value_string() if var.data_dimensions() > 1 else "",
            'units': var.get_attribute_value('units'),
        } for var in vars]

        model_dict = {
            'id': dm.id,
            'dataset': dts.id,
            'title': dts.dataset_tag,  # or use another appropriate field from Dataset
            'description': dts.text_description or dts.logical_description or "",
            'time_delta': time_delta_str,
            'objects_count': model_class.objects.count() if model_class is not None else 0,
            'file_path': "",  # Dataset doesn't have dir_path, you may need to determine this differently
            # 'file_count': model_class.objects.distinct('file_name').count() if model_class is not None else 0,
            'created': dts.created,
            'vars': var_dicts,
        }
        context['models'].append(model_dict)

    return render(request, template, context)


def technical_data(request, dataset_id):
    template = "pages/data_technical.html"
    print(request.headers)

    dts = Dataset.objects.get_or_none(id=dataset_id)
    if dts is None:
        raise Http404

    vars = Variable.objects.filter(dataset=dts).order_by(
        "non_record_variant", "name")

    context = {
        'dataset': dts,
        'dataset_attrs': DatasetAttribute.objects.filter(dataset=dts).order_by('title'),
        'vars': [{
            'var_instance': var,
            'attrs': VariableAttribute.objects.filter(variable=var).order_by('title'),
        } for var in vars]
    }

    return render(request, template, context)


def logs(request):
    template = "pages/logs.html"
    context = {}
    context['logs'] = LogEntry.objects.order_by('-timestamp')
    return render(request, template, context)
