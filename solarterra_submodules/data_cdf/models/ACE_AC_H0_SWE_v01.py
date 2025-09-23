from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class ACE_AC_H0_SWE_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    np = models.FloatField( blank=True, null=True)
    
    vp = models.FloatField( blank=True, null=True)
    
    tpr = models.FloatField( blank=True, null=True)
    
    alpha_ratio = models.FloatField( blank=True, null=True)
    
    v_gsm_vx = models.FloatField( blank=True, null=True)
    
    v_gsm_vy = models.FloatField( blank=True, null=True)
    
    v_gsm_vz = models.FloatField( blank=True, null=True)
    
    v_gse_vx = models.FloatField( blank=True, null=True)
    
    v_gse_vy = models.FloatField( blank=True, null=True)
    
    v_gse_vz = models.FloatField( blank=True, null=True)
    
    v_rtn_vr = models.FloatField( blank=True, null=True)
    
    v_rtn_vt = models.FloatField( blank=True, null=True)
    
    v_rtn_vn = models.FloatField( blank=True, null=True)
    
    sc_pos_gse_x = models.FloatField( blank=True, null=True)
    
    sc_pos_gse_y = models.FloatField( blank=True, null=True)
    
    sc_pos_gse_z = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_x = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_y = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_z = models.FloatField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

