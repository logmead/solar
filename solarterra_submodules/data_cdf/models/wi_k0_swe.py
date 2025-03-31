from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class WI_K0_SWE_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    delta_time = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day = models.IntegerField( blank=True, null=True)
    
    time_pb5_msec = models.IntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    
    mode = models.IntegerField( blank=True, null=True)
    
    sc_pos_gse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_r = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    dqf = models.IntegerField( blank=True, null=True)
    
    qf_v = models.IntegerField( blank=True, null=True)
    
    qf_vth = models.IntegerField( blank=True, null=True)
    
    qf_np = models.IntegerField( blank=True, null=True)
    
    qf_ap = models.IntegerField( blank=True, null=True)
    
    v_gse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_p_mag = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_p_lon = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_p_lat = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    thermal_spd = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    np = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    alpha_percent = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

