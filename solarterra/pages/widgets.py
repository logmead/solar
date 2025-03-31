from django import forms
from django.forms import Widget


class DateTimePicker(forms.DateTimeInput):

    template_name = "widgets/datetimepicker.html"

    class Media:
        css = {
            "all" : ["widgets/dateandtime.css"]
        }
        js = ["widgets/jquery-3.6.0.slim.min.js", "widgets/jquery.dateandtime.js" ]

class CheckboxTableGroups(forms.CheckboxSelectMultiple):

    template_name = "widgets/table_choice_groups.html"

    css = {
        "all" : ["widgets/table_choice.css"]
    }

    js = []