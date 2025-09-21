from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class INTERBALL_IT_K0_MFI_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    b_gse_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b_gse_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b_gse_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b_gsm_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b_gsm_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b_gsm_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b_abs = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    mf_delta_b = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    mf_delta_b = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sf_b = models.PositiveSmallIntegerField( blank=True, null=True)
    
    sf_mf = models.PositiveSmallIntegerField( blank=True, null=True)
    
    freq_mf_frequency = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    
    label_b_gse = models.TextField( blank=True, null=True)
    
    label_b_gsm = models.TextField( blank=True, null=True)
    
    label_mf = models.TextField( blank=True, null=True)
    
    cartesian = models.TextField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

