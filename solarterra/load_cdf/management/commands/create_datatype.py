from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.core import management
from django.utils import autoreload

from load_cdf.models import DataType
from solarterra.utils import *
from load_cdf.utils import MODEL_POSTFIX, get_django_type

# TYPE_CONVERSION = {
#     'float32': ['DecimalField', {'max_digits': '13', 'decimal_places': '6'}],
#     'float64': ['DecimalField', {'max_digits': '25', 'decimal_places': '12'}],
#     'int32': ['IntegerField'],
#     'uint8': ['PositiveSmallIntegerField'],
#     'ObjectDType': ['BigIntegerField'],
#     'StrDType': ['CharField', {'max_length': '100'}],
# }


TYPE_CONVERSION = {
    'CDF_INT1': ['SmallIntegerField'],
    'CDF_BYTE': ['SmallIntegerField'],
    'CDF_UINT1': ['PositiveSmallIntegerField'],
    'CDF_INT2': ['IntegerField'],
    'CDF_UINT2': ['PositiveIntegerField'],
    'CDF_INT4': ['IntegerField'],
    'CDF_UINT4': ['PositiveIntegerField'],
    'CDF_INT8': ['BigIntegerField'],
    'CDF_FLOAT': ['FloatField'],
    'CDF_REAL4': ['FloatField'],
    'CDF_DOUBLE': ['FloatField'],
    'CDF_REAL8': ['FloatField'],
    #'CDF_FLOAT': ['DecimalField', {'max_digits': '13', 'decimal_places': '6'}],
    #'CDF_REAL4': ['DecimalField', {'max_digits': '13', 'decimal_places': '6'}],
    #'CDF_DOUBLE': ['DecimalField', {'max_digits': '25', 'decimal_places': '12'}],
    #'CDF_REAL8': ['DecimalField', {'max_digits': '25', 'decimal_places': '12'}],
    'CDF_CHAR': ['TextField'],
    'CDF_UCHAR': ['TextField'],
    'CDF_EPOCH': ['BigIntegerField'],
    # TODO: запросить у Саши экзотику с этой хернёй
    # 'CDF_EPOCH16':,
    # 'CDF_TIME_TT2000':,
}


TYPE_DESCRIPTION = {
    'CDF_INT1': '1 байт, целое число со знаком',
    'CDF_BYTE': '1 байт, целое число со знаком',
    'CDF_UINT1': '1 байт, целое число без знака',
    'CDF_INT2': '2 байта, целое число со знаком',
    'CDF_UINT2': '2 байта, целое число без знака',
    'CDF_INT4': '4 байта, целое число со знаком',
    'CDF_UINT4': '4 байта, целое число без знака',
    'CDF_INT8': '8 байт, целое число со знаком',
    'CDF_FLOAT': '4 байта, число с плавающей запятой одинарной точности',
    'CDF_REAL4': '4 байта, число с плавающей запятой одинарной точности',
    'CDF_DOUBLE': '8 байт, число с плавающей запятой двойной точности',
    'CDF_REAL8': '8 байт, число с плавающей запятой двойной точности',
    'CDF_CHAR': '1 байт, символ',
    'CDF_UCHAR': '1 байт, беззнаковый символ',
    'CDF_EPOCH': '8 байт, число с плавающей запятой двойной точности',
    'CDF_EPOCH16': 'два по 8 байт, число с плавающей запятой двойной точности',
    'CDF_TIME_TT2000': '8 байт, целое число со знаком',
}

TYPE_FILLVAL = {
    'CDF_INT1': -128,
    'CDF_BYTE': -128,
    'CDF_UINT1': 255,
    'CDF_INT2': -32768,
    'CDF_UINT2': 65535,
    'CDF_INT4': -2147483648,
    'CDF_UINT4': 4294967295,
    'CDF_INT8': None,
    'CDF_FLOAT': -1.0e+31,
    'CDF_REAL4': -1.0e+31,
    'CDF_DOUBLE': -1.0e+31,
    'CDF_REAL8': -1.0e+31,
    'CDF_CHAR': None,
    'CDF_UCHAR': None,
    'CDF_EPOCH': -1.0e+31,
    'CDF_EPOCH16': (-1.0e+31, -1.0e+31),
    'CDF_TIME_TT2000': -9223372036854775808,
}


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument("dset_title", nargs="+", type=str)

    def handle(self, *args, **options):

        for cdf_file_label, data in TYPE_CONVERSION.items():

            datatype = DataType(
                cdf_file_label=cdf_file_label,
                description=TYPE_DESCRIPTION[cdf_file_label],
                fillval=TYPE_FILLVAL[cdf_file_label],
                django_field=data[0],
            )

            if len(data) > 1:
                datatype.max_digits = data[1].get('max_digits', None)
                datatype.max_length = data[1].get('max_length', None)
                datatype.decimal_places = data[1].get('decimal_places', None)

            datatype.save()
