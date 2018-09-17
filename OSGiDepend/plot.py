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
    _writeHeatMap(fig, folder, fileName)

def _writeHeatMap(heatmapFig, folder, fileName):
    heatmapPath = os.path.join(folder, fileName)
    heatmapFig.savefig(heatmapPath, bbox_inches = 'tight')
    plt.close(heatmapFig)

