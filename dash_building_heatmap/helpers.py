import base64
import datetime
import io
import os
import time
import copy

import pyiges
from geomdl import NURBS, BSpline, utilities
import numpy as np

import dash_html_components as html
import plotly.graph_objects as go




UPLOAD_DIRECTORY = os.path.join(os.getcwd(),'temp_iges')

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def save_temp_file(name, content) -> str:
    """
    Decode and store a file uploaded with Plotly Dash.
    saves as filename + epoch timestamp
    Remember to delete it!
    t
    Returns:
        full path as str
    """
    data = content.encode("utf8").split(b";base64,")[1]
    filepath = os.path.join(UPLOAD_DIRECTORY, name + str(time.time()))
        
    with open(filepath, "wb") as file:
        file.write(base64.decodebytes(data))
    return filepath


def _clean_iges(filepath, from_rhino = True):
    """
    this is based on export of file from rhino.
    overwrites file at filepath so create a new file (eg save_temp_file)
    """
    if not from_rhino:
        raise NotImplementedError('Good luck')

    new_lines = []

    with open(filepath, "rb") as file:
        lines = file.readlines()
        for line in lines:
            
            #TODO s = line.split()
            #if len>2 and s[-2][-1]=='P':
                #n = len(line):
                #for c in line
            line = line.replace(b'D0',b'  ')
            line = line.replace(b'D-10',b'    ')
            line = line.replace(b'D-11',b'    ')
            line = line.replace(b'D-12',b'    ')
            line = line.replace(b'D-13',b'    ')
            line = line.replace(b'D-07',b'    ')
            line = line.replace(b'D-06',b'    ')
            new_lines.append(line) # iges in expects certain things at certain chars on each line, hence replace

    with open(filepath, "wb") as file:
        file.writelines(new_lines)



def eval_bspline(b : pyiges.curves_surfaces.BSpline, delta=0.001, n = 10):
    """
    Return:
        numpy array of sampled points on bspline 
    """
    
    # Create a geomdl 3-dimensional B-spline Curve from incoming pyiges spline
    curve = NURBS.Curve()
    curve.degree = b.M
    curve.ctrlpts = b.control_points 
    curve.weights = b.W + [1]
    curve.knotvector = b.T  
    curve.delta = delta # TODO sampling - this could get out of hand depending on model dims and scale

    #TODO conditional delta: min length, n and check for straight lines

    return np.array(curve.evalpts)


def add_graphtrace_from_iges(fig : go.Figure(), filename : str = None):

    default_file = os.path.join('data', 'linework.igs')

    f = filename or default_file
    #f = save_temp_file(filename, contents) 
    _clean_iges(f)
    iges = pyiges.read(f)

    for b in iges.bsplines:
        xyz = eval_bspline(b)
        xy = list([x[:-1] for x in xyz]) #remove 3d data
        x_data = []
        y_data = []
        for c in xy:
            x_data.append(c[0])
            y_data.append(c[1])

        fig.add_trace(
            go.Scatter(
                x= x_data, 
                y= y_data,
                mode='lines',
                line =dict(color='black',width=1),
                showlegend=False
            )
        )
    return fig