from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from load_cdf.models import *


class WIND_WI_H0_MFI_v01_data(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    epoch_epoch = models.BigIntegerField( blank=True, null=True)
    
    num_pts_no_points = models.IntegerField( blank=True, null=True)
    
    bf1_b = models.FloatField( blank=True, null=True)
    
    bgse_bx = models.FloatField( blank=True, null=True)
    
    bgse_by = models.FloatField( blank=True, null=True)
    
    bgse_bz = models.FloatField( blank=True, null=True)
    
    sgsm_unit_vector_x = models.FloatField( blank=True, null=True)
    
    sgsm_unit_vector_y = models.FloatField( blank=True, null=True)
    
    sgsm_unit_vector_z = models.FloatField( blank=True, null=True)
    
    sgse_unit_vector_x = models.FloatField( blank=True, null=True)
    
    sgse_unit_vector_y = models.FloatField( blank=True, null=True)
    
    sgse_unit_vector_z = models.FloatField( blank=True, null=True)
    
    db_sc_bx = models.FloatField( blank=True, null=True)
    
    db_sc_by = models.FloatField( blank=True, null=True)
    
    db_sc_bz = models.FloatField( blank=True, null=True)
    
    tiltang_dipole_tilt = models.FloatField( blank=True, null=True)
    
    range_i_range_inner = models.FloatField( blank=True, null=True)
    
    range_o_range_outer = models.FloatField( blank=True, null=True)
    
    num3_pts_no_points = models.IntegerField( blank=True, null=True)
    
    b3f1_b = models.FloatField( blank=True, null=True)
    
    b3gse_bx = models.FloatField( blank=True, null=True)
    
    b3gse_by = models.FloatField( blank=True, null=True)
    
    b3gse_bz = models.FloatField( blank=True, null=True)
    
    num1_pts_no_points = models.IntegerField( blank=True, null=True)
    
    b1rmsf1_b_rms = models.FloatField( blank=True, null=True)
    
    b1rmsgse_bx_rms = models.FloatField( blank=True, null=True)
    
    b1rmsgse_by_rms = models.FloatField( blank=True, null=True)
    
    b1rmsgse_bz_rms = models.FloatField( blank=True, null=True)
    
    s1gse_unit_vector_x = models.FloatField( blank=True, null=True)
    
    s1gse_unit_vector_y = models.FloatField( blank=True, null=True)
    
    s1gse_unit_vector_z = models.FloatField( blank=True, null=True)
    
    time_pb5_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    brmsf1_b_rms = models.FloatField( blank=True, null=True)
    
    bgsm_bx = models.FloatField( blank=True, null=True)
    
    bgsm_by = models.FloatField( blank=True, null=True)
    
    bgsm_bz = models.FloatField( blank=True, null=True)
    
    brmsgsm_bx_rms = models.FloatField( blank=True, null=True)
    
    brmsgsm_by_rms = models.FloatField( blank=True, null=True)
    
    brmsgsm_bz_rms = models.FloatField( blank=True, null=True)
    
    brmsgse_bx_rms = models.FloatField( blank=True, null=True)
    
    brmsgse_by_rms = models.FloatField( blank=True, null=True)
    
    brmsgse_bz_rms = models.FloatField( blank=True, null=True)
    
    dist_rad_dist = models.FloatField( blank=True, null=True)
    
    pgsm_x = models.FloatField( blank=True, null=True)
    
    pgsm_y = models.FloatField( blank=True, null=True)
    
    pgsm_z = models.FloatField( blank=True, null=True)
    
    pgse_x = models.FloatField( blank=True, null=True)
    
    pgse_y = models.FloatField( blank=True, null=True)
    
    pgse_z = models.FloatField( blank=True, null=True)
    
    spc_mode_s_c_mode = models.IntegerField( blank=True, null=True)
    
    mag_mode_mfi_mode = models.IntegerField( blank=True, null=True)
    
    epoch3_epoch = models.BigIntegerField( blank=True, null=True)
    
    time3_pb5_year = models.IntegerField( blank=True, null=True)
    
    time3_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time3_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    b3rmsf1_b_rms = models.FloatField( blank=True, null=True)
    
    b3gsm_bx = models.FloatField( blank=True, null=True)
    
    b3gsm_by = models.FloatField( blank=True, null=True)
    
    b3gsm_bz = models.FloatField( blank=True, null=True)
    
    b3rmsgsm_bx_rms = models.FloatField( blank=True, null=True)
    
    b3rmsgsm_by_rms = models.FloatField( blank=True, null=True)
    
    b3rmsgsm_bz_rms = models.FloatField( blank=True, null=True)
    
    b3rmsgse_bx_rms = models.FloatField( blank=True, null=True)
    
    b3rmsgse_by_rms = models.FloatField( blank=True, null=True)
    
    b3rmsgse_bz_rms = models.FloatField( blank=True, null=True)
    
    epoch1_epoch = models.BigIntegerField( blank=True, null=True)
    
    time1_pb5_year = models.IntegerField( blank=True, null=True)
    
    time1_pb5_day_of_year = models.IntegerField( blank=True, null=True)
    
    time1_pb5_elapsed_milliseconds_of_day = models.IntegerField( blank=True, null=True)
    
    b1f1_b = models.FloatField( blank=True, null=True)
    
    b1gsm_bx = models.FloatField( blank=True, null=True)
    
    b1gsm_by = models.FloatField( blank=True, null=True)
    
    b1gsm_bz = models.FloatField( blank=True, null=True)
    
    b1rmsgsm_bx_rms = models.FloatField( blank=True, null=True)
    
    b1rmsgsm_by_rms = models.FloatField( blank=True, null=True)
    
    b1rmsgsm_bz_rms = models.FloatField( blank=True, null=True)
    
    b1gse_bx = models.FloatField( blank=True, null=True)
    
    b1gse_by = models.FloatField( blank=True, null=True)
    
    b1gse_bz = models.FloatField( blank=True, null=True)
    
    dist1_rad_dist = models.FloatField( blank=True, null=True)
    
    p1gsm_x = models.FloatField( blank=True, null=True)
    
    p1gsm_y = models.FloatField( blank=True, null=True)
    
    p1gsm_z = models.FloatField( blank=True, null=True)
    
    p1gse_x = models.FloatField( blank=True, null=True)
    
    p1gse_y = models.FloatField( blank=True, null=True)
    
    p1gse_z = models.FloatField( blank=True, null=True)
    
    s1gsm_unit_vector_x = models.FloatField( blank=True, null=True)
    
    s1gsm_unit_vector_y = models.FloatField( blank=True, null=True)
    
    s1gsm_unit_vector_z = models.FloatField( blank=True, null=True)
    

    file_name = models.CharField(max_length=100)

    objects = GetManager()

