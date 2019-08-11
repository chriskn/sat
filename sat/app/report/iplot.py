""" import plotly.plotly as py
import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


def plot_interactive_headmap():
    z = [[0.1, 0.3, 0.5], [1.0, 0.8, 0.6], [0.6, 0.4, 0.2]]

    x = ["Team A", "Team B", "Team C"]
    y = ["Game Three", "Game Two", "Game One"]

    z_text = [["Win", "Lose", "Win"], ["Lose", "Lose", "Win"], ["Win", "Win", "Lose"]]

    fig = ff.create_annotated_heatmap(
        z, x=x, y=y, annotation_text=z_text, colorscale="Viridis"
    )
    plot(fig, filename="annotated_heatmap_text")
 """
