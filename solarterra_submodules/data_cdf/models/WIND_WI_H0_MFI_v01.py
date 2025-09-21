from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class WIND_WI_H0_MFI_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch = models.BigIntegerField( blank=True, null=True)
    
    num_pts = models.IntegerField( blank=True, null=True)
    
    bf1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgse_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgse_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgse_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    brmsf1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsm_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsm_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    bgsm_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    brmsgsm_bx_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    brmsgsm_by_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    brmsgsm_bz_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    brmsgse_bx_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    brmsgse_by_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    brmsgse_bz_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    dist = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    pgsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    pgsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    pgsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    pgse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    pgse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    pgse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sgsm_unit_vector_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sgsm_unit_vector_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sgsm_unit_vector_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    sgse = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    db_sc_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    db_sc_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    db_sc_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    tiltang = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    range_i = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    range_o = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    num3_pts = models.IntegerField( blank=True, null=True)
    
    b3f1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3gse_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3gse_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3gse_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    num1_pts = models.IntegerField( blank=True, null=True)
    
    b1rmsf1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1rmsgse_bx_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1rmsgse_by_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1rmsgse_bz_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    s1gse = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    zero_i = models.TextField( blank=True, null=True)
    
    sens_i = models.TextField( blank=True, null=True)
    
    ampl_i = models.TextField( blank=True, null=True)
    
    payld_i = models.TextField( blank=True, null=True)
    
    flag_i = models.TextField( blank=True, null=True)
    
    zero_o = models.TextField( blank=True, null=True)
    
    sens_o = models.TextField( blank=True, null=True)
    
    orth_o = models.TextField( blank=True, null=True)
    
    payld_o = models.TextField( blank=True, null=True)
    
    flag_o = models.TextField( blank=True, null=True)
    
    label_time = models.TextField( blank=True, null=True)
    
    unit_time = models.TextField( blank=True, null=True)
    
    label_bgsm = models.TextField( blank=True, null=True)
    
    label_bgse = models.TextField( blank=True, null=True)
    
    label_bgsmr = models.TextField( blank=True, null=True)
    
    label_bgser = models.TextField( blank=True, null=True)
    
    label_dbsc = models.TextField( blank=True, null=True)
    
    label_pgse = models.TextField( blank=True, null=True)
    
    cartesian = models.TextField( blank=True, null=True)
    
    spc_mode = models.IntegerField( blank=True, null=True)
    
    mag_mode = models.IntegerField( blank=True, null=True)
    
    epoch3 = models.BigIntegerField( blank=True, null=True)
    
    time3_pb5_year = models.IntegerField( blank=True, null=True)
    
    time3_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time3_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    b3rmsf1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3gsm_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3gsm_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3gsm_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3rmsgsm_bx_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3rmsgsm_by_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3rmsgsm_bz_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3rmsgse_bx_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3rmsgse_by_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b3rmsgse_bz_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    epoch1 = models.BigIntegerField( blank=True, null=True)
    
    time1_pb5_year = models.IntegerField( blank=True, null=True)
    
    time1_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time1_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    b1f1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1gsm_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1gsm_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1gsm_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1rmsgsm_bx_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1rmsgsm_by_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1rmsgsm_bz_rms = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1gse_bx = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1gse_by = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    b1gse_bz = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    dist1 = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    p1gsm_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    p1gsm_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    p1gsm_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    p1gse_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    p1gse_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    p1gse_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    s1gsm_unit_vector_x = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    s1gsm_unit_vector_y = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    s1gsm_unit_vector_z = models.DecimalField(max_digits=13,decimal_places=6, blank=True, null=True)
    
    orth_i = models.TextField( blank=True, null=True)
    
    ampl_o = models.TextField( blank=True, null=True)
    
    format_time = models.TextField( blank=True, null=True)
    
    label_pgsm = models.TextField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

