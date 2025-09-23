from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class INTERBALL_IT_K0_MFI_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    b_gse_bx = models.FloatField( blank=True, null=True)
    
    b_gse_by = models.FloatField( blank=True, null=True)
    
    b_gse_bz = models.FloatField( blank=True, null=True)
    
    b_gsm_bx = models.FloatField( blank=True, null=True)
    
    b_gsm_by = models.FloatField( blank=True, null=True)
    
    b_gsm_bz = models.FloatField( blank=True, null=True)
    
    b_abs = models.FloatField( blank=True, null=True)
    
    mf_delta_b_1_4hz = models.FloatField( blank=True, null=True)
    
    mf_delta_b_600_850hz = models.FloatField( blank=True, null=True)
    
    sf_b = models.PositiveSmallIntegerField( blank=True, null=True)
    
    sf_mf = models.PositiveSmallIntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

