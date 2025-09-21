from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class INTERBALL_IT_K0_ELE_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    ne = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    te = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    ne1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    te1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    flag_el = models.PositiveSmallIntegerField( blank=True, null=True)
    
    gap_flag = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

