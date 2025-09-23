from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class INTERBALL_IT_K0_VDP_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    fi = models.FloatField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

