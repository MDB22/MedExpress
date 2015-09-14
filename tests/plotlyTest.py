import plotly.plotly as py
import numpy as np
from plotly.graph_objs import *

import plotly.plotly as py
import pandas as pd

##scatter = dict(
##    mode = "markers",
##    name = "y",
##    type = "scatter3d",    
##    x = df['x'], y = df['y'], z = df['z'],
##    marker = dict( size=2, color="rgb(23, 190, 207)" )
##)
##
##x = np.array([-1, 1, 1, -1])
##y = np.array([-1, -1, -1, -1])
##z = np.array([-1, -1, 1, 1])
##
##scatter = dict(
##    mode = "markers",
##    name = "y",
##    type = "scatter3d",    
##    x = x, y = y, z = z,
##    marker = dict( size=2, color="rgb(23, 190, 207)" )
##)
##
##clusters = dict(
##    alphahull = 7,
##    name = "y",
##    opacity = 0.1,
##    type = "mesh3d",    
##    x = x, y = y, z = z
##)
##
##layout = dict(
##    title = '3d point clustering'
##)
##
##print(clusters)

##df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/alpha_shape.csv')
##df.head()

df = dict(
    x = pd.Series([-1, 1, 1, -1, -1, 1, 1, -1]),
    y = pd.Series([-1, -1, -1, -1, 1, 1, 1, 1]),
    z = pd.Series([-1, -1, 1, 1, -1, -1, 1, 1])
)

scatter = dict(
    mode = "markers",
    type = "scatter3d",    
    x = df['x'], y = df['y'], z = df['z'],
    marker = dict( size=2, color="rgb(23, 190, 207)" )
)
clusters = dict(
    alphahull = 7,
    opacity = 0.1,
    type = "mesh3d",    
    x = df['x'], y = df['y'], z = df['z']
)
layout = dict(
    title = '3d point clustering'
)

fig = dict( data=[scatter, clusters], layout=layout )

url = py.plot(fig, filename='Testing surface', validate=False, auto_open=False)

print url
