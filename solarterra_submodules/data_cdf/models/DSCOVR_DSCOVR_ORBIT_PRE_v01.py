from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class DSCOVR_DSCOVR_ORBIT_PRE_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    sun_r = models.FloatField( blank=True, null=True)
    
    gci_pos_x = models.FloatField( blank=True, null=True)
    
    gci_pos_y = models.FloatField( blank=True, null=True)
    
    gci_pos_z = models.FloatField( blank=True, null=True)
    
    gci_vel_vx = models.FloatField( blank=True, null=True)
    
    gci_vel_vy = models.FloatField( blank=True, null=True)
    
    gci_vel_vz = models.FloatField( blank=True, null=True)
    
    gse_pos_x = models.FloatField( blank=True, null=True)
    
    gse_pos_y = models.FloatField( blank=True, null=True)
    
    gse_pos_z = models.FloatField( blank=True, null=True)
    
    moon_gse_pos_moon_x = models.FloatField( blank=True, null=True)
    
    moon_gse_pos_moon_y = models.FloatField( blank=True, null=True)
    
    moon_gse_pos_moon_z = models.FloatField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

