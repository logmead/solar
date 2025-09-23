from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class WIND_WI_K0_SWE_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    mode = models.IntegerField( blank=True, null=True)
    
    sc_pos_gsm_x = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_y = models.FloatField( blank=True, null=True)
    
    sc_pos_gsm_z = models.FloatField( blank=True, null=True)
    
    qf_np = models.IntegerField( blank=True, null=True)
    
    qf_ap = models.IntegerField( blank=True, null=True)
    
    v_gse_vx = models.FloatField( blank=True, null=True)
    
    v_gse_vy = models.FloatField( blank=True, null=True)
    
    v_gse_vz = models.FloatField( blank=True, null=True)
    
    v_gsm_vx = models.FloatField( blank=True, null=True)
    
    v_gsm_vy = models.FloatField( blank=True, null=True)
    
    v_gsm_vz = models.FloatField( blank=True, null=True)
    
    v_gse_p_flow_speed = models.FloatField( blank=True, null=True)
    
    v_gse_p_e_w_flow = models.FloatField( blank=True, null=True)
    
    v_gse_p_n_s_flow = models.FloatField( blank=True, null=True)
    
    thermal_spd = models.FloatField( blank=True, null=True)
    
    np = models.FloatField( blank=True, null=True)
    
    alpha_percent = models.FloatField( blank=True, null=True)
    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    delta_time = models.FloatField( blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_millisecond_of_day = models.IntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    
    sc_pos_gse_x = models.FloatField( blank=True, null=True)
    
    sc_pos_gse_y = models.FloatField( blank=True, null=True)
    
    sc_pos_gse_z = models.FloatField( blank=True, null=True)
    
    sc_pos_r = models.FloatField( blank=True, null=True)
    
    dqf = models.IntegerField( blank=True, null=True)
    
    qf_v = models.IntegerField( blank=True, null=True)
    
    qf_vth = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

