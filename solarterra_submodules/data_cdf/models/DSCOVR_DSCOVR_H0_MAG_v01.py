from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class DSCOVR_DSCOVR_H0_MAG_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch1 = models.BigIntegerField( blank=True, null=True)
    
    time1_pb5_year = models.IntegerField( blank=True, null=True)
    
    time1_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time1_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    num1_pts = models.IntegerField( blank=True, null=True)
    
    b1f1 = models.FloatField( blank=True, null=True)
    
    b1sdf1 = models.FloatField( blank=True, null=True)
    
    b1gse_bx = models.FloatField( blank=True, null=True)
    
    b1gse_by = models.FloatField( blank=True, null=True)
    
    b1gse_bz = models.FloatField( blank=True, null=True)
    
    b1sdgse_bx_sigma = models.FloatField( blank=True, null=True)
    
    b1sdgse_by_sigma = models.FloatField( blank=True, null=True)
    
    b1sdgse_bz_sigma = models.FloatField( blank=True, null=True)
    
    b1rtn_br = models.FloatField( blank=True, null=True)
    
    b1rtn_bt = models.FloatField( blank=True, null=True)
    
    b1rtn_bz = models.FloatField( blank=True, null=True)
    
    b1sdrtn_br_sigma = models.FloatField( blank=True, null=True)
    
    b1sdrtn_bt_sigma = models.FloatField( blank=True, null=True)
    
    b1sdrtn_bz_sigma = models.FloatField( blank=True, null=True)
    
    range1 = models.IntegerField( blank=True, null=True)
    
    flag1 = models.IntegerField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

