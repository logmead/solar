from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class SPEKTRR_SPR_K0_BMSW_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    vp = models.FloatField( blank=True, null=True)
    
    tp = models.FloatField( blank=True, null=True)
    
    np = models.FloatField( blank=True, null=True)
    
    nanp = models.FloatField( blank=True, null=True)
    
    qual = models.PositiveSmallIntegerField( blank=True, null=True)
    
    st_flag = models.PositiveSmallIntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

