import math


# points per plot, golden ratio
PPP = 1500

# all these functions work with bigints
def get_bin_size(ts_limits):
    """
    to get bin size, i need to:
        get timedelta in seconds
        split timedelta on how many points per plot
    
    """

    time_delta = ts_limits[1] - ts_limits[0]
    bin_size = math.ceil(time_delta / PPP)
    print("IN BIN")
    print(ts_limits[1] + bin_size)
    return bin_size, (ts_limits[0], ts_limits[1] + bin_size)

