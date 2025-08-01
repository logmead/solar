from django.core.exceptions import ValidationError
from data_cdf.models import *
from load_cdf.models import Experiment
from django import forms
from pages.widgets import DateTimeWidget, DateTimePicker, CheckboxTableGroups
import datetime as dt
from django.db.models import Q



class SourceForm(forms.Form):

    sources = forms.MultipleChoiceField(
        label="Загруженные наборы данных",
        choices=Experiment.objects.form_choices(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )


    ts_start = forms.DateTimeField(
        label="От",
        required=True,
        widget=DateTimeWidget(attrs={'id' : "dtw_start"})
    )

    ts_end = forms.DateTimeField(
        label="До",
        required=True,
        widget=DateTimeWidget(attrs={'id' : "dtw_end"})
    )

    def clean(self):
        cleaned_data = super().clean()
        ts_start = cleaned_data.get("ts_start")
        ts_end = cleaned_data.get("ts_end")

        if ts_start >= ts_end:
            raise ValidationError("Start time should be before end time.")


class VariablesForm(forms.Form):

    variables = forms.MultipleChoiceField(
        label="Выберите переменные для построения",
        choices=('',''),
        widget=CheckboxTableGroups(),
    )

    ts_start = forms.DateTimeField(
        required=False,
        widget=forms.HiddenInput()
    )

    ts_end = forms.DateTimeField(
        required=False,
        widget=forms.HiddenInput()
    )


    def __init__(self, *args, **kwargs):

        render_flag = kwargs.get('render_flag', True)
        if 'render_flag' in kwargs:
            del kwargs['render_flag']

        exp_instances = kwargs.get('exp_instances', None)
        if 'exp_instances' in kwargs:
            del kwargs['exp_instances']

        # timestmap tuples in 
        ts_tuple = kwargs.get('ts_tuple', None)
        if 'ts_tuple' in kwargs:
            del kwargs['ts_tuple']
        
        super().__init__(*args, **kwargs)

        if exp_instances is not None:
            
            var_choices = []
            print(f"limits in form {ts_tuple}")
            
            if render_flag:
                print("full_render")
                for exp in exp_instances:
                    
                    obj = exp.dynamic.resolve_class().objects.all()

                    time_field = exp.dynamic.get_time_fields().first().field_name
                    print(f"IN FORM TIMEFIELD {time_field}")
                    kwargs = { 
                        '{0}__gte'.format(time_field) : ts_tuple[0],
                        '{0}__lte'.format(time_field) : ts_tuple[1],
                    }
                    total_quantity = obj.filter(**kwargs).count()

                    exp_vars = exp.variables.filter(is_data=True)
                    var_fields = []
                    for exp_var in exp_vars:
                        
                        if exp_var.has_depends():
                            time_field_name = exp_var.dynamic.first().get_time_field_name()

                            field_name = exp_var.dynamic.first()
                            
                            kwargs = {
                                '{0}__gte'.format(time_field_name) : ts_tuple[0],
                                '{0}__lte'.format(time_field_name) : ts_tuple[1],
                                '{0}__isnull'.format(field_name): False 
                                }
                            quantity = obj.filter(**kwargs).count()
                            # print(f"has_depends {time_field_name} {field_name} {quantity}")
                            var_fields.append((exp_var.id , (exp_var.get_description(), quantity)))
                    var_choices.append(((exp.get_description(), total_quantity), var_fields))
                self.fields['variables'].choices = var_choices

            else:
                print("partial_render")
                for exp in exp_instances:
                    exp_vars = exp.variables.filter(is_data=True)
                    var_fields = [ (exp_var.id, exp_var.get_description()) for exp_var in exp_vars ]
                    var_choices.append((exp.get_description(), var_fields))

            # print("managed to set choices~", var_choices)
                self.fields['variables'].choices = var_choices


