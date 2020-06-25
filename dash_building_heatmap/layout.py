#builtin modules
import os

import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np

import helpers

DATA_PATH = os.path.join(os.getcwd(),'data')


def layout(filename = None):
    #TODO load multiple csv into a hidden div in the background as cache.
    #TODO ouline of building, stair core from cad file. 
    file = filename or 'a_p0w_h024sh0.csv'
    csv_path = os.path.join(DATA_PATH,file)

    df = pd.read_csv(csv_path,skip_blank_lines=True)

    def clean(i : float, b: bool, gridsize : float =0.5):
        """
        removes weird 0.0000000001 from coord data.
        would be better removed at source (in GH) for performance
        """
        if b:
            i=-i


        if i <0.01:
            return 0

            
        i = 1000* int(i/gridsize) * gridsize
        return i

    def mirror(l):
        m = max(l)
        return l.apply(lambda x: m-x) 

    rad_data = df['radiation']
    x_data = df['x'].apply(lambda x:clean(x,True))
    y_data = df['y'].apply(lambda x:clean(x,False))

    y_data = mirror(y_data)


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


    fig = helpers.add_graphtrace_from_iges(fig)

    return dcc.Graph(figure=fig)