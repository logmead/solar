import datetime as dt
import string
import re
from pytz import UTC


# time work

def make_aware(ts):
    return ts.replace(tzinfo=UTC)


# translates datetime instance into bigint
def ts_bigint_resolver(ts):
    return int(ts.timestamp())
    

# translates number into the datetime instance
def bigint_ts_resolver(num):
    return dt.datetime.fromtimestamp(num, UTC)

def str_to_dt(st, template="%Y-%m-%d %H:%M:%S"):
    return dt.datetime.strptime(st, template)

# here numbers are passed
def get_neighbour_interval(ts_limits, next_interval=True):

    t_delta = ts_limits[1] - ts_limits[0]
    if next_interval:
        return (ts_limits[1], ts_limits[1] + t_delta)
    else:
        return (ts_limits[0] - t_delta, ts_limits[0])


# string work
def normalize_str(st):
    return st.strip().replace(' ', '_')


def remove_parenthesis(st):
    return re.sub(r'\([^)]*\)', '', st).strip()

#also think about removing all repeating parts of the suffix strings

def safe_str(st):
    allowed = string.ascii_lowercase + string.digits + '_'
    parsed = normalize_str(remove_parenthesis(st)).lower()
    return ''.join(filter(lambda x: x in allowed, parsed))
