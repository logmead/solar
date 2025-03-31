from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class WI_OR_PRE_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day = models.IntegerField( blank=True, null=True)
    
    time_pb5_msec = models.IntegerField( blank=True, null=True)
    
    gci_pos_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gci_pos_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gci_pos_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gci_vel_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gci_vel_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gci_vel_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gse_pos_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gse_pos_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gse_pos_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gse_vel_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gse_vel_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gse_vel_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gsm_pos_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gsm_pos_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gsm_pos_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gsm_vel_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gsm_vel_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    gsm_vel_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    sun_vector_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    sun_vector_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    sun_vector_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    hec_pos_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    hec_pos_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    hec_pos_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    hec_vel_x = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    hec_vel_y = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    hec_vel_z = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    crn_earth = models.IntegerField( blank=True, null=True)
    
    long_earth = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    lat_earth = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    long_space = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    
    lat_space = models.DecimalField(max_digits=25,decimal_places=12, blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

