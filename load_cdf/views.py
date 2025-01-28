from django.shortcuts import render
from django.http import Http404
from load_cdf.models import Experiment, ExperimentAttribute, ExperimentAttributeValue,\
    Variable, VariableAttribute, VariableAttributeValue

# Create your views here.

# def experiment_metadata(request):
#     template = "load_cdf/experiment_meta_table.html"
#     context = dict()
#     exps = Experiment.objects.order_by("-created")
    
#     context['exp_data'] = [{
#         'exp_instance' : exp,
#         'attrs' : ExperimentAttribute.objects.filter(experiment=exp).order_by('title'),
#     } for exp in exps ]

#     return render(request, template, context)

# def variable_metadata(request, experiment_id):
#     template = "load_cdf/variable_meta.html"
#     context = dict()

#     exp = Experiment.objects.get_or_none(id=experiment_id)
#     print(exp)
#     if exp is None:
#         raise Http404

#     context['exp'] = exp
#     vars = Variable.objects.filter(experiment=exp).order_by("non_record_variant", "name")
#     context['var_data'] = [{
#         'var_instance' : var,
#         'attrs' : VariableAttribute.objects.filter(variable=var),
#     } for var in vars ]

#     return render(request, template, context)