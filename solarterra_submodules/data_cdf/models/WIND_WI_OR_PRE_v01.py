from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class WIND_WI_OR_PRE_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_ms_of_day = models.IntegerField( blank=True, null=True)
    
    gci_pos_x = models.FloatField( blank=True, null=True)
    
    gci_pos_y = models.FloatField( blank=True, null=True)
    
    gci_pos_z = models.FloatField( blank=True, null=True)
    
    gci_vel_vx = models.FloatField( blank=True, null=True)
    
    gci_vel_vy = models.FloatField( blank=True, null=True)
    
    gci_vel_vz = models.FloatField( blank=True, null=True)
    
    gse_vel_vx = models.FloatField( blank=True, null=True)
    
    gse_vel_vy = models.FloatField( blank=True, null=True)
    
    gse_vel_vz = models.FloatField( blank=True, null=True)
    
    hec_pos_x = models.FloatField( blank=True, null=True)
    
    hec_pos_y = models.FloatField( blank=True, null=True)
    
    hec_pos_z = models.FloatField( blank=True, null=True)
    
    long_earth = models.FloatField( blank=True, null=True)
    
    lat_space = models.FloatField( blank=True, null=True)
    
    gse_pos_x = models.FloatField( blank=True, null=True)
    
    gse_pos_y = models.FloatField( blank=True, null=True)
    
    gse_pos_z = models.FloatField( blank=True, null=True)
    
    gsm_pos_x = models.FloatField( blank=True, null=True)
    
    gsm_pos_y = models.FloatField( blank=True, null=True)
    
    gsm_pos_z = models.FloatField( blank=True, null=True)
    
    gsm_vel_vx = models.FloatField( blank=True, null=True)
    
    gsm_vel_vy = models.FloatField( blank=True, null=True)
    
    gsm_vel_vz = models.FloatField( blank=True, null=True)
    
    sun_vector_sun_x = models.FloatField( blank=True, null=True)
    
    sun_vector_sun_y = models.FloatField( blank=True, null=True)
    
    sun_vector_sun_z = models.FloatField( blank=True, null=True)
    
    hec_vel_vx = models.FloatField( blank=True, null=True)
    
    hec_vel_vy = models.FloatField( blank=True, null=True)
    
    hec_vel_vz = models.FloatField( blank=True, null=True)
    
    crn_earth = models.IntegerField( blank=True, null=True)
    
    lat_earth = models.FloatField( blank=True, null=True)
    
    long_space = models.FloatField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

