from django.db import models
import uuid
from solarterra.abstract_models import GetManager
from django.apps import apps
from load_cdf.utils import TYPE_CONVERSION
from django.conf import settings
from django.db.models import Max, Min
from solarterra.utils import bigint_ts_resolver

# ------------filesystem work-----------------#


class Upload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    zip_path = models.CharField(max_length=300)
    zip_md5 = models.CharField(max_length=100, blank=True, null=True)

    #  goes after the dataset tag in zipname (for WIND_WIND_OR_PRE_v01_u1 it would be 1)
    human_tag = models.CharField(max_length=200)

    result_status = models.PositiveSmallIntegerField(
        default=1,  # in case of sudden interruptions in code, i want to give SUCCESS status manually
        choices=[
            (0, "Success"),
            (1, "Unexpected error"),
            (2, "Collision in filenames")
            # 📌 more to be added
        ])

    # how many files were found, provided by processing script
    file_count = models.PositiveIntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True) # not needed if we are keeping failed uploads

    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="uploads")

    objects = GetManager()

    def __str__(self):
        # id doesn't matter and human tag is not unique
        return str(self.created) + "_" + self.human_tag


class CDFFileStored(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # the name of the file
    full_path = models.CharField(max_length=300)

    # the upload it belongs to
    upload = models.ForeignKey(
        "Upload", on_delete=models.CASCADE, related_name="CDFfiles")

    objects = GetManager()

    def __str__(self):
        return self.file_name


# ------------datasets---------------------#
'''
    Dataset is a collection of CDF files that share the same 
    match file. It is identified by a DATASET_TAG
    which is also the full path to the directory where the files are stored.
'''


class DatasetManager(GetManager):

    def form_choices(self):
        return [(exp.id, exp.get_description) for exp in self.all()]


class Dataset(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # the tag is the name of the directory where the files are stored + the name of the match file
    # e.g. WIND_WIND_OR_PRE_v01
    dataset_tag = models.CharField(max_length=100, unique=True)

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
        return self.dataset_tag

    def get_uploads_list(self):
        return self.uploads.all()

    def get_attribute_value(self, attribute_title):
        attr = self.attributes.filter(title__iexact=attribute_title).first()
        if attr:
            return attr.get_value()
        else:
            return None

    # def get_description(self):

    #     subs = ["project", "descriptor", "data_type"]

    #     lsd = self.get_attribute_value('Logical_source_description')
    #     if lsd is not None:
    #         return lsd
    #     else:
    #         return ", ".join([self.get_attribute_value(sub) for sub in subs])


class DatasetAttribute(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=100)
    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="attributes")

    unique_values = models.PositiveIntegerField()
    unique_for_file = models.BooleanField()

    objects = GetManager()

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
    data_type = models.CharField(max_length=100)
    shape = models.CharField(max_length=100)
    non_record_variant = models.BooleanField()

    # what is the var_type attribute
    is_data = models.BooleanField(default=False)

    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="variables")

    objects = GetManager()
    """
    dataset fk
    variable title
    number of files it is in 
    """

    def __str__(self):
        return self.name

    def data_dimensions(self):
        return len(self.shape.strip('(),').split(','))

    def has_depends(self):
        depends = VariableAttributeValue.objects.filter(
            attribute__variable=self, attribute__title__icontains='depend')
        if depends.count() == 0:
            return False
        else:
            return True

    def dependency_vars(self):

        depends = VariableAttributeValue.objects\
            .filter(attribute__variable=self, attribute__title__icontains='depend')\
            .values_list('value', flat=True)
        return self.dataset.variables.filter(name__in=list(depends))

    def dependency_nrv_var(self):
        potentials = self.dependency_vars().filter(non_record_variant=True)
        if potentials.count() == 1:
            return potentials.first()
        else:
            print("There is no single NRV dependency.")

    def nrv_in_order(self):
        # order is a part of VariableDataNRV
        return self.nrv_values.order_by('order')

    def nrv_value_string(self):
        return f"[{' '.join(self.nrv_in_order().values_list('value', flat=True))}]"

    def is_datetime(self):
        return True if self.data_type == 'ObjectDType' else False

    def is_decimal(self):
        return True if 'float' in self.data_type else False

    def get_precision(self):
        if self.is_decimal():
            record = TYPE_CONVERSION[self.data_type][1]
            return int(record['decimal_places']), int(record['max_digits'])
        else:
            return None

    def get_attribute_value(self, attribute_title, get_type=False):
        attr = self.attributes.filter(title__iexact=attribute_title).first()
        if attr:
            if get_type:
                return attr.get_value(), attr.data_type
            else:
                return attr.get_value()
        else:
            return None

    def get_description(self):
        desc = self.get_attribute_value('catdesc')
        if desc is not None:
            return desc
        else:
            return self.get_attribute_value('fieldnam')

    def get_axis_label(self):

        units = self.get_attribute_value('units')
        if units:
            return f"{self.name}, {units}"
        else:
            return self.name

    def is_log(self):
        scaletype = self.get_attribute_value('scaletyp')
        if scaletype is not None and scaletype == "log":
            print(f"YAY {self.name} is LOG!")
            return True
        else:
            return False


class VariableDataNRV(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    value = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField()
    variable = models.ForeignKey(
        "Variable", on_delete=models.CASCADE, related_name="nrv_values")

    objects = GetManager()

    class Meta:
        unique_together = ('variable', 'order',)


class VariableAttribute(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    variable = models.ForeignKey(
        "Variable", on_delete=models.CASCADE, related_name="attributes")

    unique_values = models.PositiveIntegerField()

    objects = GetManager()

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
        "Dataset", on_delete=models.CASCADE, related_name="dynamic")
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

    # if field is exploded, then some nrv data was used here
    nrv_instance = models.ForeignKey(
        "VariableDataNRV", on_delete=models.CASCADE, related_name="dynamic_field", blank=True, null=True)

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


def make_log_entry(code, message, upload=None, addition=None, color='black'):

    STANDARD_COLORS = {
        "START": 'blue',
        "EXIT": 'blue',
        "WARNING": 'yellow',
        "ERROR": 'red',
        "OK": 'green',
        "FINISHED": 'green'
    }
    if code in STANDARD_COLORS:
        color = STANDARD_COLORS[code]

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
