#builtin modules
import os

import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd


DATA_PATH = os.path.join(os.getcwd(),'data')


def layout(filename = None):
    #TODO load multiple csv into a hidden div in the background as cache.
    #TODO ouline of building, stair core from cad file. 
    file = filename or 'a_p8w_h818l_s0.75d_b_s2sh0.csv'
    csv_path = os.path.join(DATA_PATH,file)

    df = pd.read_csv(csv_path,skip_blank_lines=True)

    def clean(i : float):
        """
        removes weird 0.0000000001 from coord data.
        would be better removed at source (in GH) for performance
        """
        if i <0.01:
            return 0
        return i 

    rad_data = df['radiation']
    x_data = df['x'].apply(lambda x:clean(x))
    y_data = df['y'].apply(lambda x:clean(x))

    #TODO do colorbar units and title.
    #TODO hover unit and title.
    fig = go.Figure(data=go.Heatmap(
            showscale = True,
            zmin = 0,
            zmax= rad_data.max(),
            z=rad_data,
            x=x_data,
            y=y_data,))

    # TODO remove background rto lyaout and tidy up axes.
 
    fig['layout'].update(
        autosize=False,
        yaxis=dict(scaleanchor="x", scaleratio=1)
        )

    return dcc.Graph(figure=fig)