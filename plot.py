import plotly.graph_objs as go
import plotly
from flask import Markup
colors = ['#1cc88a', '#36b9cc', '#4e73df', '#f6c23e', '#e74a3b']

def pie(title, labels, values, hole=.5):
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        hoverinfo="label+percent",
        text=labels,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2))
    )])

    fig.layout.title = title
    fig.layout.font = dict(family='Nunito', size=18, color='#858796')

    return Markup(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'))
