from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class {{ name }}(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    {% for field in fields %}
    {{ field.title }} = models.{{ field.django_type }}({% if field.max_length %}max_length={{ field.max_length }},{% endif %}{% if field.max_digits %}max_digits={{ field.max_digits }},{% endif %}{% if field.decimal_places %}decimal_places={{ field.decimal_places }},{% endif %} blank=True, null=True)
    {% endfor %}

    file_name = models.CharField(max_length=100)

    objects = GetManager()

