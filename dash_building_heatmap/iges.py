import base64
import datetime
import io
import os
import time


import pyiges
from geomdl import NURBS, BSpline, utilities
import numpy as np

import dash_html_components as html



UPLOAD_DIRECTORY = os.path.join(os.getcwd(),'temp_iges')

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def save_temp_file(name, content) -> str:
    """
    Decode and store a file uploaded with Plotly Dash.
    saves as filename + epoch timestamp
    Remember to delete it!
    
    Returns:
        full path as str
    """
    data = content.encode("utf8").split(b";base64,")[1]
    filepath = os.path.join(UPLOAD_DIRECTORY, name + str(time.time()))
        
    with open(filepath, "wb") as file:
        file.write(base64.decodebytes(data))
    return filepath


def clean_iges(filepath):
    new_lines = []

    with open(filepath, "rb") as file:
        lines = file.readlines()
        print ('hello')
        for line in lines:
            s = line.split()
            if len>2 and s[-2][-1]=='P':
                n = len(line):
                

                
                for c in line
            line = line.replace('D0','  ')
            line = line.replace('D-10','    ')
            line = line.replace('D-11','    ')
            line = line.replace('D-12','    ')
            line = line.replace('D-13','    ')
            new_lines.append(line)

    with open(filepath, "wb") as file:
        file.writelines(new_lines)



def eval_bspline(b : pyiges.curves_surfaces.BSpline, delta=0.1):
    # Create a 3-dimensional B-spline Curve
    curve = NURBS.Curve()
    curve.degree = b.M
    curve.ctrlpts = b.control_points  # Set control points (weights vector will be 1 by default)
    curve.weights = b.W + [1]
    curve.knotvector = b.T  # Set knot vector
    curve.delta = delta

    return np.array(curve.evalpts)


