from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from django.apps import apps
from load_cdf.utils import TYPE_CONVERSION
from django.conf import settings
from django.db.models import Max, Min
from solarterra.utils import bigint_ts_resolver
import os

# ------------filesystem work-----------------#


class Upload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    zip_path = models.CharField(max_length=300)
    zip_md5 = models.CharField(max_length=100, blank=True, null=True)

    #  goes after the dataset tag in zipname (for WIND_WIND_OR_PRE_v01_u123 it would be 123)
    u_tag = models.CharField(max_length=200)

    result_status = models.PositiveSmallIntegerField(
        default=1,  # in case of sudden interruptions in code, i want to give SUCCESS status manually
        choices=[
            (0, "Success"),
            (1, "Unexpected error"),
            (2, "Collision in filenames"),
            (3, "Match file error")
            # 📌 more to be added
        ])

    # how many files were found, provided by processing script
    file_count = models.PositiveIntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True) # not needed if we are keeping failed uploads

    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="uploads", blank=True, null=True)

    objects = GetManager()

    class Meta:
        unique_together = ['u_tag', 'dataset']

    def __str__(self):
        # id doesn't matter and human tag is not unique
        return str(self.created) + "_" + self.u_tag

    def get_cdfs(self):
        return self.CDFfiles.all()

    def get_logs(self):
        return self.logs.all()

    def ifZipAlive(self):
        # check if the zip file is still alive
        return os.path.exists(self.zip_path)

    def clean_up(self):
        # currently removes only the zip file
        # might be extended to remove empty directories or somesuch
        if self.ifZipAlive():
            os.remove(self.zip_path)


class CDFFileStored(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # the name of the file
    full_path = models.CharField(max_length=300)

    # the upload it belongs to
    upload = models.ForeignKey(
        "Upload", on_delete=models.CASCADE, related_name="CDFfiles")

    objects = GetManager()

    def __str__(self):
        return self.full_path


# ------------datasets---------------------#
'''
    Dataset is a collection of CDF files that share the same 
    match file. It is identified by a DATASET_TAG
    which is also the full path to the directory where the files are stored.
'''


class DatasetManager(GetManager):

    def form_choices(self):
        return [(dts.id, dts.get_description()) for dts in self.all()]


class Dataset(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # the tag is the name of the directory where the files are stored + the name of the match file
    # e.g. WIND_WIND_OR_PRE_v01
    tag = models.CharField(max_length=100, unique=True)

    # global attributes from match file - tag parts
    mission = models.CharField(max_length=100)
    source_name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    instrument = models.CharField(max_length=100)
    dataset_version = models.CharField(max_length=100)

    # global attributes from match file - dataset description
    text_description = models.TextField(blank=True, null=True)
    logical_source = models.CharField(max_length=200, blank=True, null=True)
    logical_description = models.TextField(blank=True, null=True)
    pi_name = models.CharField(max_length=200, blank=True, null=True)
    pi_affiliation = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = DatasetManager()

    def __str__(self):
        return self.tag

    def get_uploads_list(self):
        return self.uploads.all()

    def get_attribute_value(self, attribute_title):
        attr = self.attributes.filter(title__iexact=attribute_title).first()
        if attr:
            return attr.get_value()
        else:
            return None

    def get_description(self):
        # Try text_description first, then logical_description, then build from components
        # might be better to use logical first
        if self.text_description:
            return self.text_description
        elif self.logical_description:
            return self.logical_description
        else:
            # Fallback to dataset_tag or build from components
            return self.tag


class DatasetAttributeManager(GetManager):
    def is_standartized(self, **kwargs):
        return self.filter(**kwargs).filter(linked_standard_field__isnull=False)


class DatasetAttribute(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=100)
    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="attributes", blank=True, null=True)

    linked_standard_field = models.CharField(
        max_length=100, blank=True, null=True)  # name of the field in Dataset model

    def is_standartized(self):
        return self.linked_standard_field is not None

    objects = DatasetAttributeManager()

    def __str__(self):
        return self.title

    def get_value(self):
        return self.values.first().value

    """
    for the file attributes that are in all files:

    title of the attribute 
    experiment fk
    number of values 
    """


class DatasetAttributeValue(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    value = models.TextField(blank=True, null=True)
    attribute = models.ForeignKey(
        "DatasetAttribute", on_delete=models.CASCADE, related_name="values")

    objects = GetManager()

# ------------demarcation to vars---------------------#


'''
    Variable is a single variable in dataset CDF files.
'''


class VariableManager(GetManager):
    pass
    # def form_choices(self):
    #     return [(var.id, var.get_description()) for var in self.filter(non_record_variant=False) ]


class Variable(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)

    # -------MFLBL fields--------

    # original cdf datatype, before conversion to Django
    # TYPE_CONVERSION table is currently in utils.py
    # TODO: should be taken from cdaweb manual
    datatype = models.CharField(max_length=200, blank=True, null=True)

    dims = models.SmallIntegerField(blank=True,null=True)
    # TODO костыль, пока у нас нет спектрограмм
    dim_sizes = models.SmallIntegerField(blank=True,null=True)

    is_displayed = models.BooleanField(blank=True,null=True, default=False)

    # this one for future use, currently 3 values ['time', 'orbit', 'NA']
    data_category = models.CharField(max_length=200,blank=True, null=True)

    # -----MF fields------

    catdesc = models.CharField(max_length=200,blank=True, null=True)
    var_notes = models.TextField(blank=True, null=True)
    depend_0 = models.CharField(max_length=200,blank=True, null=True)
    display_type = models.CharField(max_length=200,blank=True, null=True)
    fillval = models.CharField(max_length=200,blank=True, null=True)
    output_format = models.CharField(max_length=200,blank=True, null=True)
    lablaxis = models.CharField(max_length=200,blank=True, null=True)

    units = models.CharField(max_length=200,blank=True, null=True)
    # char bc it depends on units
    validmin = models.CharField(max_length=200,blank=True, null=True)
    validmax = models.CharField(max_length=200,blank=True, null=True)
    # VAR_TYPE
    var_logic_type = models.CharField(max_length=200,blank=True, null=True)
    scaletyp = models.CharField(max_length=200,blank=True, null=True)
    scalemin = models.CharField(max_length=200,blank=True, null=True)
    scalemax = models.CharField(max_length=200,blank=True, null=True)

    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="variables")

    objects = VariableManager()

    def __str__(self):
        return self.name

    def is_data(self):
        return var_logic_type.lower() == 'data'


class VariableAttribute(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=100)
    # can it be determined from cdf_file?
    # do i even use it?
    data_type = models.CharField(max_length=100, blank=True, null=True)

    variable = models.ForeignKey(
        "Variable", on_delete=models.CASCADE, related_name="attributes")
    linked_standard_field = models.CharField(
        max_length=100, blank=True, null=True)  # name of the field in Dataset model

    # reflects dimensionality of a variable
    multipart = models.BooleanField(blank=True, null=True)

    objects = GetManager()

    def is_Standartized(self):
        return self.linked_standard_field is not None

    def get_value(self):
        return self.values.first().value

    def __str__(self):
        return self.title


class VariableAttributeValue(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    value = models.TextField(blank=True, null=True)
    attribute = models.ForeignKey(
        "VariableAttribute", on_delete=models.CASCADE, related_name="values")

    objects = GetManager()

# ------------demarcation to dynamic models---------------------#

# TODO: describe DynamicModel and DynamicField


class DynamicModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # string reference to existing MODEL
    model_name = models.CharField(max_length=100)

    # actual Dataset it is made for
    dataset_instance = models.OneToOneField(
        "Dataset", on_delete=models.CASCADE, related_name="dynamic", blank=True, null=True)
    model_file_path = models.TextField()

    objects = GetManager()

    def __str__(self):
        return self.model_name

    def get_time_fields(self):
        return self.fields.filter(variable_instance__name__icontains="epoch")

    def resolve_class(self):
        try:
            model_class = apps.get_model(
                app_label='data_cdf', model_name=self.model_name)
            return model_class
        except:
            return None

    def get_time_limits(self, to_datetime=True):
        time_field_name = self.get_time_fields().first().field_name
        model_class = self.resolve_class()
        if model_class is not None and model_class.objects.count() > 1:
            ts_limits = model_class.objects.aggregate(
                max=Max(time_field_name), min=Min(time_field_name))
            if to_datetime:
                t_start = bigint_ts_resolver(ts_limits['min'])
                t_end = bigint_ts_resolver(ts_limits['max'])
                return t_start, t_end
            else:
                return ts_limits['min'], ts_limits['max']
        else:
            return None, None


class DynamicField(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # string reference to existing MODEL FIELD
    field_name = models.CharField(max_length=100)

    # is it made from multiple vars?
    exploded = models.BooleanField()

    # actual variable instance it represents
    variable_instance = models.ForeignKey(
        "Variable", on_delete=models.CASCADE, related_name="dynamic")

    dynamic_model = models.ForeignKey(
        "DynamicModel", on_delete=models.CASCADE, related_name="fields")

    objects = GetManager()

    def __str__(self):
        return self.field_name

    def get_time_field(self):
        time_var = self.variable_instance.dependency_vars().filter(
            name__icontains='epoch').first()
        if time_var is not None:
            return time_var.dynamic.first()
        else:
            return None

    def get_time_field_name(self):
        time_field = self.get_time_field()
        if time_field is not None:
            return time_field.field_name
        else:
            return None

# ------------demarcation to logging---------------------#

# might be in need of complete reworking


class LogEntry(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    timestamp = models.DateTimeField(auto_now_add=True)
    upload = models.ForeignKey(
        "Upload", on_delete=models.CASCADE, related_name="logs", blank=True, null=True)
    code = models.CharField(max_length=15, null=True, blank=True)
    color = models.CharField(max_length=15, null=True, blank=True)
    message = models.TextField()
    addition = models.TextField(blank=True, null=True)

    objects = GetManager()

    def __str__(self):
        return f"{self.timestamp} {self.code}"

    def to_file(self):
        s = f"{self.timestamp.strftime('%H:%M:%S %d.%m.%Y')}    "
        if self.code:
            s += f"[{self.code}]  "
        s += self.message
        return s + "\n"


# upload is optional, because some logs may not be related to uploads
def make_log_entry(code, message, upload=None, addition=None, color=None):

    # note: in ideal world, color palette should be in settings.py or @ css somewhere
    STANDARD_COLORS = {
        "START": 'blue',
        "EXIT": 'blue',
        "WARNING": 'yellow',
        "ERROR": 'red',
        "OK": 'green',
        "SUCCESS": 'green',
        "CREATED": 'green',
        "DELETED": 'red'
    }

    if not color and code in STANDARD_COLORS:
        color = STANDARD_COLORS[code]
    else:
        color = 'black'

    entry = LogEntry(
        code=code,
        message=message,
        color=color,
        addition=addition,
        upload=upload
    )
    entry.save()
    with open(settings.LOG_FILE, mode="a") as f:
        f.write(entry.to_file())
