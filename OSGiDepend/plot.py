import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns 
import os
sns.set()
DPI = 72.27

def plotHeatmap(dataFrame, title, folder, fileName):
    fontsize_pt = plt.rcParams['ytick.labelsize']
    numberOfEntries = dataFrame.shape[0]
    # compute the required figure height 
    matrix_height_pt = fontsize_pt * numberOfEntries
    matrix_height_in = matrix_height_pt / DPI
    entryOffset = numberOfEntries * 0.2
    figure_height = matrix_height_in + entryOffset
    # colors
    colorMap = plt.get_cmap('autumn_r', 10)
    colorMap.set_under('white')
    colorMap.set_over('black')
    tenPercent = int(round(numberOfEntries * 0.1))
    maxTenPercent = sorted(dataFrame.values.flatten())[-tenPercent:]
    vmax = min(maxTenPercent)
    # build figure
    fig, ax = plt.subplots(figsize=(figure_height,figure_height))
    ax.set_title(title)
    # add heatmap
    sns.heatmap(dataFrame, square=True, fmt="d", ax=ax, 
        xticklabels=True, yticklabels=True,
        annot_kws={"size": 8}, annot=True,
        cbar_kws={"shrink": 0.5}, 
        cmap=colorMap, vmin=1, vmax=vmax,
        linewidths=0.5, linecolor="grey"
    )
    _writeFigure(fig, folder, fileName)

def plotStackedBarChart(data, yLabel, folder, fileName):
    column0 = data[data.columns[0]].values
    column1 = data[data.columns[1]].values
    total = column0 + column1
    data["total"] = total
    # Set general plot properties
    sns.set_style("white")
    sns.set_context({"figure.figsize": (24, 10)})
    # Plot 1 - background - "total" (top) series
    sns.barplot(x = data.index, y = data.total, color = "red")
    # Plot 2 - overlay - "bottom" series
    bottom_plot = sns.barplot(x = data.index, y = column0, color = "green")
    topbar = plt.Rectangle((0,0),1,1,fc="red", edgecolor = 'none')
    bottombar = plt.Rectangle((0,0),1,1,fc='green',  edgecolor = 'none')
    l = plt.legend([bottombar, topbar], [data.columns[0], 'Total'], loc=1, ncol=2, prop={'size':16})
    l.draw_frame(False)
    # Optional - Make plot look nicer
    sns.despine(left=True)
    for label in bottom_plot.get_xticklabels():
        if len(label._text) > 60:
            label._text = "..."+label._text[-60:]
    bottom_plot.set_xticklabels(bottom_plot.get_xticklabels(), rotation=90)
    bottom_plot.set_ylabel(yLabel)
    _writeFigure(bottom_plot.get_figure(),folder, fileName)

def _writeFigure(figure, folder, fileName):
    path = os.path.join(folder, fileName)
    figure.savefig(path, bbox_inches = 'tight')
    plt.close(figure)