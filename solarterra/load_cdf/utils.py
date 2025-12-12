import datetime as dt
import math

MODEL_POSTFIX = "_data"

TYPE_CONVERSION = {}
#     'float32' : ['DecimalField', {'max_digits' : '13', 'decimal_places' : '6'}],
#     'float64' : ['DecimalField', {'max_digits' : '25', 'decimal_places' : '12'}],
#     'int32' : ['IntegerField'],
#     'uint8' : ['PositiveSmallIntegerField'],
#     'ObjectDType' : ['BigIntegerField'],
#     'StrDType' : ['CharField', {'max_length' : '100'}],
# }
"""
TYPE_CONVERSION = {
    'CDF_INT1': ,
    'CDF_BYTE': ,
    'CDF_UINT1': ,
    'CDF_INT2': ,
    'CDF_UINT2': ,
    'CDF_INT4': ,
    'CDF_UINT4': ,
    'CDF_INT8': ,
    'CDF_FLOAT': ,
    'CDF_REAL4': ,
    'CDF_DOUBLE': ,
    'CDF_REAL8': ,
    'CDF_CHAR': ,
    'CDF_UCHAR': ,
    'CDF_EPOCH': ,
    'CDF_EPOCH16': ,
    'CDF_TIME_TT2000': ,
}
"""


def one_d_len(shape):
    return int(shape.strip('(),'))

#obsolete since we have DataType class now
# def get_django_type(some_type):
#     if some_type in TYPE_CONVERSION.keys():
#         result = TYPE_CONVERSION[some_type]
#         return result[0], result[1] if len(result) > 1 else {}
#     else:
#         return None

def get_django_type(some_type):
    datatype_obj = DataType.objects.get_or_none(cdf_file_label = some_type)
    if datatype_obj:
        result = datatype_obj.django_field
        return result
    else:
        return None

def make_type(value, type_name):
    #converts value to it's "true" type for python handling
    #TODO: floats should probably be rounded to the output_format precision
    if 'int' in type_name:
        return int(value)
    elif 'datetime' in type_name:
        return dt.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    else:
        return value

# # float errors handling
# def convert_format_to_persicion(format_str):
#     if format_str:
#         after_point = int(format_str.split('.')[1])
#         return 10**(-after_point)
#     else: return None