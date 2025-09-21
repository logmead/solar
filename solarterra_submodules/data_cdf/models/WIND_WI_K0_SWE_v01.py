from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class WIND_WI_K0_SWE_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    mode = models.IntegerField( blank=True, null=True)
    
    sc_pos_gsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    qf_np = models.IntegerField( blank=True, null=True)
    
    unit_time = models.TextField( blank=True, null=True)
    
    label_time = models.TextField( blank=True, null=True)
    
    format_time = models.TextField( blank=True, null=True)
    
    label_pos_gse = models.TextField( blank=True, null=True)
    
    label_pos_gsm = models.TextField( blank=True, null=True)
    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    delta_time = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_millisecond_of_day = models.IntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    
    sc_pos_gse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_r = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    dqf = models.IntegerField( blank=True, null=True)
    
    qf_v = models.IntegerField( blank=True, null=True)
    
    qf_vth = models.IntegerField( blank=True, null=True)
    
    qf_ap = models.IntegerField( blank=True, null=True)
    
    v_gse_vx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_vy = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_vz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gsm_vx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gsm_vy = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gsm_vz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_p_flow_speed = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_p_e_w_flow = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    v_gse_p_n_s_flow = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    thermal_spd = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    np = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    alpha_percent = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    label_v_gse = models.TextField( blank=True, null=True)
    
    label_v_gsm = models.TextField( blank=True, null=True)
    
    label_v_polar = models.TextField( blank=True, null=True)
    
    unit_polar = models.TextField( blank=True, null=True)
    
    cartesian = models.TextField( blank=True, null=True)
    
    polar = models.TextField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

