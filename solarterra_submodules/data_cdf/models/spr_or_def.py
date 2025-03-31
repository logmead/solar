from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class SPR_OR_DEF_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    sc_pos_gse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    reg = models.PositiveSmallIntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

