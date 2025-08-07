from data_cdf.models import *
from load_cdf.models import Dataset
from django import forms
from pages.widgets import DateTimePicker, CheckboxTableGroups
import datetime as dt
from django.db.models import Q


class SourceForm(forms.Form):

    sources = forms.MultipleChoiceField(
        label="Загруженные наборы данных",
        choices=Dataset.objects.form_choices(),
        widget=forms.CheckboxSelectMultiple()
    )

    ts_start = forms.DateTimeField(
        label="От",
        required=False,
        widget=forms.DateTimeInput()
    )

    ts_end = forms.DateTimeField(
        label="До",
        required=False,
        widget=forms.DateTimeInput()
    )


class VariablesForm(forms.Form):

    variables = forms.MultipleChoiceField(
        label="Выберите переменные для построения",
        choices=('', ''),
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

        dataset_instances = kwargs.get('dataset_instances', None)
        if 'dataset_instances' in kwargs:
            del kwargs['dataset_instances']

        # timestmap tuples in
        ts_tuple = kwargs.get('ts_tuple', None)
        if 'ts_tuple' in kwargs:
            del kwargs['ts_tuple']

        super().__init__(*args, **kwargs)

        if dataset_instances is not None:

            var_choices = []
            print(f"limits in form {ts_tuple}")

            if render_flag:
                print("full_render")
                for dts in dataset_instances:

                    obj = dts.dynamic.resolve_class().objects.all()

                    time_field = dts.dynamic.get_time_fields().first().field_name
                    print(f"IN FORM TIMEFIELD {time_field}")
                    kwargs = {
                        '{0}__gte'.format(time_field): ts_tuple[0],
                        '{0}__lte'.format(time_field): ts_tuple[1],
                    }
                    total_quantity = obj.filter(**kwargs).count()

                    dataset_vars = dts.variables.filter(is_data=True)
                    var_fields = []
                    for dataset_var in dataset_vars:

                        if dataset_var.has_depends():
                            time_field_name = dataset_var.dynamic.first().get_time_field_name()

                            field_name = dataset_var.dynamic.first()

                            kwargs = {
                                '{0}__gte'.format(time_field_name): ts_tuple[0],
                                '{0}__lte'.format(time_field_name): ts_tuple[1],
                                '{0}__isnull'.format(field_name): False
                            }
                            quantity = obj.filter(**kwargs).count()
                            # print(f"has_depends {time_field_name} {field_name} {quantity}")
                            var_fields.append(
                                (dataset_var.id, (dataset_var.get_description(), quantity)))
                    var_choices.append(
                        ((dts.get_description(), total_quantity), var_fields))
                self.fields['variables'].choices = var_choices

            else:
                print("partial_render")
                for dts in dataset_instances:
                    dataset_vars = dts.variables.filter(is_data=True)
                    var_fields = [(dataset_var.id, dataset_var.get_description())
                                  for dataset_var in dataset_vars]
                    var_choices.append((dts.get_description(), var_fields))

            # print("managed to set choices~", var_choices)
                self.fields['variables'].choices = var_choices
