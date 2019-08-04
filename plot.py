import plotly.graph_objs as go
import plotly
from flask import Markup

def pie(labels, values, hole=.3):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=hole)])
    return Markup(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'))
