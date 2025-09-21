from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class ACE_AC_H0_MFI_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    magnitude = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsec_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsec_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsec_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsm_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsm_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsm_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    dbrms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    q_flag = models.IntegerField( blank=True, null=True)
    
    sc_pos_gse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    label_bgse = models.TextField( blank=True, null=True)
    
    label_bgsm = models.TextField( blank=True, null=True)
    
    label_pos_gse = models.TextField( blank=True, null=True)
    
    label_pos_gsm = models.TextField( blank=True, null=True)
    
    unit_time = models.TextField( blank=True, null=True)
    
    label_time = models.TextField( blank=True, null=True)
    
    format_time = models.TextField( blank=True, null=True)
    
    cartesian = models.TextField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

