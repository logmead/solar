from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class ACE_AC_OR_SSC_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    gse_lat = models.FloatField( blank=True, null=True)
    
    gse_lon = models.FloatField( blank=True, null=True)
    
    radius = models.FloatField( blank=True, null=True)
    
    xyz_gse_x = models.FloatField( blank=True, null=True)
    
    xyz_gse_y = models.FloatField( blank=True, null=True)
    
    xyz_gse_z = models.FloatField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

