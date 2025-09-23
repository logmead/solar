from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class SPEKTRR_SPR_OR_DEF_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    sc_pos_gse_x = models.FloatField( blank=True, null=True)
    
    sc_pos_gse_y = models.FloatField( blank=True, null=True)
    
    sc_pos_gse_z = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_x = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_y = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_z = models.FloatField( blank=True, null=True)
    
    reg = models.PositiveSmallIntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

