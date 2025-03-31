import plotly.graph_objects as go
from plotly.subplots import make_subplots


def scatter(q_params, p_params, data):

    fig = go.Figure()

    field = q_params['list_of_fieldnames'][0]
    print("LOOKING AT FIELDS")
    # for field in q_params['list_of_fieldnames']:
    #     print(field)

    fig.add_trace(go.Scatter(x=data['dt_timestamp'], y=data[field], connectgaps=False, mode="lines+markers"))


    fig.update_traces(connectgaps=False, marker=dict(size=4))
    ts = p_params['ts_limits_dt']
    fig.update_layout(
        xaxis_range=[ts[0], ts[1]],
        yaxis_title=q_params['var_instance'].get_axis_label(),
        )
    
    if q_params['var_instance'].is_log():
        fig.update_yaxes(type="log")

    config = {'displayModeBar': False}
    plot_div=fig.to_html(config=config, full_html=False, div_id=f"plot_div_{q_params['var_id']}", default_width="100%")
    

    return plot_div


def n_trace(q_params, p_params, data):

    fields = q_params['list_of_fieldnames']

    fig = make_subplots(rows=len(fields), cols=1, shared_xaxes=True, vertical_spacing=0.05)
    ts = p_params['ts_limits_dt']
    for index, field in enumerate(fields):
        fig.add_trace(go.Scatter(
                x=data['dt_timestamp'], 
                y=data[field], 
                connectgaps=False, 
                mode="lines+markers",
                ),
            row=index + 1,
            col=1
            )
        
        fig['layout'][f"yaxis{index+1}"]['title'] = field
        fig['layout'][f"xaxis{index+1}"]['range'] = [ts[0], ts[1]]
    
    fig.update_traces(marker=dict(size=4))

    
    fig.update_layout(
        height=700,
        xaxis_range=[ts[0], ts[1]],
        showlegend=False,
        )

    config = {'displayModeBar': False}
    plot_div=fig.to_html(config=config, full_html=False, div_id=f"plot_div_{q_params['var_id']}", default_width="100%")

    return plot_div
