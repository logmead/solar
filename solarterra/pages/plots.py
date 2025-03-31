
from pages.figures import scatter, n_trace
from solarterra.utils import bigint_ts_resolver as its

import pandas as pd
import numpy as np
import datetime as dt
import math

"""
can change query kwargs to f-string format

"""



# points per plot, golden ratio
PPP = 700

# all these functions work with bigints
def get_bin_size(ts_limits):
    """
    to get bin size, i need to:
        get timedelta in seconds
        split timedelta on how many points per plot
    
    """

    time_delta = ts_limits[1] - ts_limits[0]
    bin_size = math.ceil(time_delta / PPP)

    return bin_size, (ts_limits[0], ts_limits[1] + bin_size)




def get_query_params(variable):
    fields = variable.dynamic.all()

    q_params = {
        'var_instance' : variable,
        'var_id' : variable.id,
        'is_multiple': True if fields.count() > 1 else False,
        'list_of_fieldnames' : fields.values_list('field_name', flat=True),
        'time_field_name' : fields.first().get_time_field_name(),
        'model_class' : variable.experiment.dynamic.resolve_class(),
    }
    
    return q_params


def get_plot(qs, p, q_params):
    print("IN BINNING")
    
    complete_df = None

    field_count = len(q_params['list_of_fieldnames'])

    for field in q_params['list_of_fieldnames']:
        print(field)
        time_field = q_params['time_field_name']
        qu = qs.filter(**{'{0}__isnull'.format(field) : False})
        if qu.count() == 0:
            if field_count == 1:
                return None
            else:
                continue
        just_values = qu.values_list(field, time_field)

       
        rn  = np.array(just_values)
        
        rns = rn[rn[:, 1].argsort()]
        
        v_arr = rns.T[0]
        t_arr = rns.T[1]
        
        idx = np.argsort(t_arr)
        idxs = np.searchsorted(p['t'], t_arr[idx], side='right')


        full_1 = np.c_[idxs, v_arr]
        # print(full_1)

        groups_1 = full_1[:, 0].copy()
        full_1 = np.delete(full_1, 0, axis=1)
        _ndx_1 = np.argsort(groups_1)
        _id1, _pos1, g_count_1 = np.unique(groups_1[_ndx_1], return_index=True, return_counts=True)

        g_sum_1 = np.add.reduceat(full_1[_ndx_1], _pos1, axis=0)
        g_mean_1 = g_sum_1 / g_count_1[:, None]

        res_1 = np.c_[_id1, g_mean_1]
        # print(res_1)
        # print(f"lens full {full_1.shape} res {res_1.shape}")

        
        df = pd.DataFrame(data={field : res_1.T[1]}, index=res_1.T[0])

        # del extras
        del qu, just_values
        del rn, rns, idx, idxs
        del full_1, groups_1, _ndx_1, _id1, _pos1
        del g_count_1, g_sum_1, g_mean_1, res_1
        
       
        new_df = df.reindex(p['t_df_index'])
        if complete_df is None:
            complete_df = new_df
        else:
            complete_df[field] = new_df[field]
        # print(new_df)
        # print(new_df.shape)
        

    complete_df[time_field] = p['tm']
    complete_df['dt_timestamp'] = complete_df.apply(lambda x: its(x[time_field]), axis=1)
    
    # print(f"final df shape is {complete_df.shape}")
    # print(complete_df)
    
    # print("LOOKING AT")
    # ar = arrays[field]
    # new_ar = np.diff(ar[idx].cumsum()[idxs])/np.diff(idxs)
    # print(new_ar[:30])
    if field_count > 1:
        return n_trace(q_params, p, complete_df)
    else:
        return scatter(q_params, p, complete_df)


def get_queryset(qp, ts_limits):
    
    
    kwargs = {
        '{0}__gte'.format(qp['time_field_name']) : ts_limits[0],
        '{0}__lte'.format(qp['time_field_name']) : ts_limits[1],
    }
    queryset = qp['model_class'].objects.filter(**kwargs)
    print("QUERYSET PREFORMING")
    print(ts_limits[0], ts_limits[1])
    print(queryset.count())
    
    return queryset

# returns a list of plots with all the info required
def get_plots(variables, ts_limits, ts_limits_dt):
    complete_list = []

    plot_params = {
        'ts_limits' : ts_limits,
        'ts_limits_dt' : ts_limits_dt,
    }


    plot_params['bin_size'], plot_params['new_ts_limits'] = get_bin_size(ts_limits)
    plot_params['bin_size_dt'] = dt.timedelta(seconds=plot_params['bin_size'])
    plot_params['hbs'] = math.ceil(plot_params['bin_size'] / 2)
    plot_params['t'] = np.arange(plot_params['new_ts_limits'][0], plot_params['new_ts_limits'][1], step=plot_params['bin_size'])
    plot_params['t_df_index'] = np.arange(1, plot_params['t'].size)
    plot_params['tm'] = np.arange(plot_params['t'][0] + plot_params['hbs'], plot_params['t'][-1], step=plot_params['bin_size'])


    for var in variables:
        
        query_params = get_query_params(var)
        print("QUERY_PARAMS")
        print(query_params)
        queryset = get_queryset(query_params, ts_limits)


        plot = get_plot(queryset, plot_params, query_params)
        
        complete_list.append({
            'instance' : var,
            'plot' : plot,
        })
        

    return complete_list, plot_params
    