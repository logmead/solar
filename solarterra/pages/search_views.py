from django.shortcuts import render
from load_cdf.models import DynamicModel, DynamicField, Variable, LogEntry, Experiment, ExperimentAttribute, VariableAttribute
from data_cdf.models import *
from django.http import Http404
from django.apps import apps
from solarterra.utils import bigint_ts_resolver
from pages.forms import  SourceForm, VariablesForm
import datetime as dt
from solarterra.utils import ts_bigint_resolver as tsi, bigint_ts_resolver as its, str_to_dt, get_neighbour_interval as gni
from pages.plots import get_plots

def search(request):
    template = "pages/forms/source_form.html"
    context = {}

    if request.method == 'POST':
        print(request.POST)
        source_form = SourceForm(data=request.POST)
        if source_form.is_valid():
            print("valid!")
            context['form'] = source_form
            context['success'] = True
            
        else:
            print("invalid!")
            context['form'] = source_form
            context['success'] = False
    else:
        dyn = DynamicModel.objects.first()
        ts_start, ts_end = dyn.get_time_limits()
        context['form'] = SourceForm(initial={'ts_start' : ts_start, 'ts_end' : ts_end})

    return render(request, template, context)

def variables(request):

    template = "pages/forms/vars_form.html"
    context = {}

    # dyn = DynamicModel.objects.first()
    # limits = dyn.get_time_limits(to_datetime=False)
    # print(f"limits in view {limits}")

    if request.method == 'POST':
        print(request.POST)
        source_form = SourceForm(data=request.POST)
        if source_form.is_valid():
            print("request is valid!!")
            sources  = source_form.cleaned_data['sources']
            ts_start_dt  = source_form.cleaned_data['ts_start']
            ts_end_dt  = source_form.cleaned_data['ts_end']
            ts_start  = tsi(ts_start_dt)
            ts_end  = tsi(ts_end_dt)
            
            exp_instances = Experiment.objects.filter(id__in=sources)
            
            context['var_form'] = VariablesForm(
                exp_instances=exp_instances, 
                ts_tuple=(ts_start, ts_end), 
                initial={'ts_start' : ts_start_dt, 'ts_end' : ts_end_dt}
                )
            return render(request, template, context)
        else:
            print("variables form invalid!")

    raise Http404
    # return render(request, template, context)




def plot(request):

    template = "pages/plot_page.html"

    context = {}
    

    if request.method == 'POST':
        #print(request.POST)
        ts_start_dt = str_to_dt(request.POST['ts_start'])
        ts_end_dt = str_to_dt(request.POST['ts_end'])

        ts_tuple_dt = (ts_start_dt, ts_end_dt)
        ts_tuple = (tsi(ts_start_dt), tsi(ts_end_dt))
        variables_form = VariablesForm(
            render_flag=False,
            exp_instances=Experiment.objects.all(),
            ts_tuple=ts_tuple,
            data=request.POST
        )
        
        
        if variables_form.is_valid():
            variables_list = variables_form.cleaned_data['variables']
            #print(type(variables_list), variables_list)
            var_instances = Variable.objects.filter(id__in=variables_list)
            var_list = list(var_instances.values_list('id', flat=True))
            
            context['complete_list'], context['plot_params']  = get_plots(var_instances, ts_tuple, ts_tuple_dt)

            ex_ids = var_instances.distinct('experiment').values_list('experiment', flat=True)
            exp_instances = Experiment.objects.filter(id__in=ex_ids)
            #print(exp_instances)
            prev_tuple = gni(ts_tuple, next_interval=False)
            prev_tuple_dt = (its(prev_tuple[0]), its(prev_tuple[1]))
            next_tuple = gni(ts_tuple, next_interval=True)
            next_tuple_dt = (its(next_tuple[0]), its(next_tuple[1]))
            
            context['ts_tuple'] = ts_tuple_dt

            """
            two forms of type VariableForm (rendered as invisible) with 
                neighbouring time interval initials set
                the same list of variable ids selected 
            """

            context['prev_form'] = {
                    'form' : VariablesForm(
                    exp_instances=exp_instances, 
                    ts_tuple=prev_tuple, 
                    initial={'ts_start' : prev_tuple_dt[0], 'ts_end' : prev_tuple_dt[1], 'variables' : var_list}
                    ),
                    'id' : 'prev-form-id'
                }
                
            context['next_form'] = {
                    'form' : VariablesForm(
                    exp_instances=exp_instances, 
                    ts_tuple=next_tuple, 
                    initial={'ts_start' : next_tuple_dt[0], 'ts_end' : next_tuple_dt[1], 'variables' : var_list}
                    ),
                    'id' : 'next-form-id'
            }
                

        
            return render(request, template, context)

    raise Http404
