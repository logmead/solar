from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class INTERBALL_IT_OR_DEF_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    sc_pos_gse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_pos_gsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_vel_gse_vx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_vel_gse_vy = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sc_vel_gse_vz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    scss_sep_gse_delta_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    scss_sep_gse_delta_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    scss_sep_gse_delta_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sf_sc_sep = models.PositiveSmallIntegerField( blank=True, null=True)
    
    cartesian = models.TextField( blank=True, null=True)
    
    label_pos_gse = models.TextField( blank=True, null=True)
    
    label_pos_gsm = models.TextField( blank=True, null=True)
    
    label_vel_gse = models.TextField( blank=True, null=True)
    
    label_sep_gse = models.TextField( blank=True, null=True)
    
    sf_sc_orbit = models.PositiveSmallIntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

