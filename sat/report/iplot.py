# pylint: disable=W0611
# unused import

import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


def heatmap(x_labels, y_labels, values):
    fig = ff.create_annotated_heatmap(
        z=values, x=x_labels, y=y_labels, colorscale="Reds", showscale=True
    )
    plot(fig, filename="labelled-heatmap")


def barchart():
    data = [go.Bar(x=["giraffes", "orangutans", "monkeys"], y=[20, 14, 23])]

    plot(data, filename="basic-bar")


def stacked_barchart():
    trace1 = go.Bar(
        x=["giraffes", "orangutans", "monkeys"], y=[20, 14, 23], name="SF Zoo"
    )
    trace2 = go.Bar(
        x=["giraffes", "orangutans", "monkeys"], y=[12, 18, 29], name="LA Zoo"
    )

    data = [trace1, trace2]
    layout = go.Layout(barmode="stack")

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename="stacked-bar")
