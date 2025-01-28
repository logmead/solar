from django.shortcuts import render
from load_cdf.models import DynamicModel, DynamicField, Variable, LogEntry, Experiment, ExperimentAttribute, VariableAttribute
from data_cdf.models import *
from django.http import Http404
from django.apps import apps
from solarterra.utils import bigint_ts_resolver
from django.db.models import Max, Min
from django.conf import settings
from django.db import connection


def main_page(request):
    template = "pages/main.html"
    context = {"main_page" : True}
    return render(request, template, context)


def system_data(request):
    template = "pages/system_data.html"
    cursor = connection.cursor()
    cursor.execute('select version();')
    row = cursor.fetchone() 
    context = {
        'version' : settings.PROJECT_VERSION,
        'path' : settings.BASE_DIR,
        'hashsum' : '',
        'db_version' : row[0],
   
    }

    return render(request, template, context)


def data_info(request):
    template = "pages/data_official.html"
    context = {
    "models" : []       
    }

    dynamic_models = DynamicModel.objects.order_by('-experiment_instance__created')
    for dm in dynamic_models:
        model_class = dm.resolve_class()
        exp = dm.experiment_instance

        # check loading script for wi_ho consistency with times

        ts_start_limit, ts_end_limit = dm.get_time_limits()
        t_start = ts_start_limit.date() if ts_start_limit else ""
        t_end = ts_end_limit.date() if ts_end_limit else ""
        time_delta_str =  f"{t_start}  -  {t_end}" 
    
        
        # multidim = var.get_attribute_value('depend_1')

        vars = dm.experiment_instance.variables.filter(non_record_variant=False)
        var_dicts = [ {
            'name' : var.name,
            'description' : var.get_attribute_value('fieldnam'),
            'data_type' : var.is_data,
            'depends_on' : var.get_attribute_value('depend_0'),
            'multidim' : var.dependency_nrv_var().nrv_value_string() if var.data_dimensions() > 1 else "",
            'units' : var.get_attribute_value('units'),
        } for var in vars ]
        

        

        model_dict = {
            'id' : dm.id,
            'experiment' : exp.id,
            'title' : exp.technical_title,
            'description': exp.get_description(),
            'time_delta' : time_delta_str,
            'objects_count' : model_class.objects.count() if model_class is not None else 0,
            'file_path': exp.dir_path,
            #'file_count': model_class.objects.distinct('file_name').count() if model_class is not None else 0,
            'created' : exp.created,
            'vars' : var_dicts,
        }
        context['models'].append(model_dict)


    return render(request, template, context)


def technical_data(request, exp_id):
    template = "pages/data_technical.html"
    print(request.headers)

    exp = Experiment.objects.get_or_none(id=exp_id)
    if exp is None:
        raise Http404
    
    vars = Variable.objects.filter(experiment=exp).order_by("non_record_variant", "name")

    context = {
        'exp' : exp,
        'exp_attrs' : ExperimentAttribute.objects.filter(experiment=exp).order_by('title'),
        'vars' : [{
            'var_instance' : var,
            'attrs' : VariableAttribute.objects.filter(variable=var).order_by('title'),
        } for var in vars ]
    }
    
    return render(request, template, context)

def logs(request):
    template = "pages/logs.html"
    context = {}
    context['logs'] = LogEntry.objects.order_by('-timestamp')
    return render(request, template, context)


