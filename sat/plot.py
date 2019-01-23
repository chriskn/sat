import pandas as pd
import matplotlib.pyplot as plt
import logging
import seaborn as sns
import squarify
import os
import numpy as np
from collections import OrderedDict


sns.set()

_DPI = 72.27
_LOGGER = logging.getLogger(__name__)
_MAX_HEATMAP_ENTRIES = 200
_MAX_TREEMAP_ENTRIES = 25


def plot_heatmap(data_frame, title, folder, file_name):
    number_of_entries = data_frame.shape[0]
    if number_of_entries > _MAX_HEATMAP_ENTRIES:
        _LOGGER.warn("Number of entries is %d and exceeds limit of %d for heatmaps. Will skip creation of heatmap" % (
            number_of_entries, _MAX_HEATMAP_ENTRIES))
        return
    fontsize_pt = plt.rcParams['ytick.labelsize']
    # compute the required figure height
    matrix_height_pt = fontsize_pt * number_of_entries * 1.02
    matrix_height_in = matrix_height_pt / _DPI
    entry_offset = number_of_entries * 0.2
    figure_size = int(round(matrix_height_in + entry_offset))
    # colors
    color_map = plt.get_cmap('autumn_r', 10)
    # build figure
    fig, ax = plt.subplots(figsize=(figure_size, figure_size))
    ax.set_title(title)
    # plot
    sns.heatmap(data_frame, square=True, fmt="d", ax=ax,
                xticklabels=True, yticklabels=True,
                annot_kws={"size": 8}, annot=True,
                cbar_kws={"shrink": 0.5},
                cmap=color_map,
                # vmin=1, vmax=vmax,
                linewidths=0.5, linecolor="grey"
                )
    _writeFigure(fig, folder, file_name)


def _wrap_label(label, length):
    labellines = []
    offset = 5
    towrap = label
    while len(towrap) > length+offset:
        l, r = towrap[:length], towrap[length:]
        labellines.extend([l, r])
        towrap = r
    return "\n".join(labellines)


def plot_treemap(data, title, folder, file_name, value_name):
    width = 700.
    height = 433.
    # restrict number of values
    number_of_entries = data.shape[0]
    if number_of_entries > _MAX_TREEMAP_ENTRIES:
        _LOGGER.warn("Number of entries  (%d) exceeds limit for treemaps. Will limit to max %d values" % (
            len(data), _MAX_TREEMAP_ENTRIES))
    names = data[data.columns[0]].values
    values = data[data.columns[1]].values
    labels = []
    for index, pname in enumerate(names):
        label = pname
        if len(pname) > 30:
            label = _wrap_label(names, 25)
        value = values[index]
        label = "\n".join([label, value_name+" "+"%.2f" % round(value, 2)])
        labels.append(label)
    # the sum of the values must equal the total area to be laid out
    # i.e., sum(values) == width * height
    norm_values = squarify.normalize_sizes(values, width, height)
    # colors
    color_map = plt.get_cmap('autumn_r', len(labels))
    colors = [color_map(i) for i in range(len(norm_values))][::-1]
    # plot
    plt.rc('font', size=8)
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111)
    ax = squarify.plot(sizes=norm_values, color=colors,
                       label=labels, ax=ax, alpha=.7)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=16)
    # color bar
    img_data = np.array(values)
    img_data = np.expand_dims(img_data, axis=0)
    img = plt.imshow(img_data, cmap=color_map)
    img.set_visible(False)
    fig.colorbar(img, orientation="vertical", shrink=.96)
    _writeFigure(plt.gcf(), folder, file_name)


def plot_stacked_barchart(data, ylabel, title, folder, file_name):
    labels = data[data.columns[0]].values
    data_column_1 = data.columns[1]
    data_column_2 = data.columns[2]
    column_data_1 = data[data_column_1].values
    column_data_2 = data[data_column_2].values
    total = column_data_1 + column_data_2
    # Set general plot properties
    sns.set_style("white")
    sns.set_context({"figure.figsize": (24, 10)})
    # Plot 1 - background - "total" (top) series
    sns.barplot(x=labels, y=total, color="red")
    # Plot 2 - overlay - "bottom" series
    bottom_plot = sns.barplot(x=labels, y=column_data_1, color="green")
    # Legend
    top_bar = plt.Rectangle((0, 0), 1, 1, fc="red", edgecolor='none')
    bottom_bar = plt.Rectangle((0, 0), 1, 1, fc='green',  edgecolor='none')
    legend = plt.legend([bottom_bar, top_bar], [data_column_1,
                                                data_column_2], loc=1, ncol=2, prop={'size': 16})
    legend.draw_frame(False)
    bottom_plot.set_ylabel(ylabel)
    bottom_plot.set_title(title)
    # remove spines
    sns.despine(left=True)
    # trim labels
    for label in bottom_plot.get_xticklabels():
        if len(label._text) > 40:
            label._text = "..."+label._text[-40:]
    # rotate labels
    bottom_plot.set_xticklabels(bottom_plot.get_xticklabels(), rotation=80)
    _writeFigure(bottom_plot.get_figure(), folder, file_name)

def plot_barchart(data, ylabel, title, folder, filename):
    if data.empty:
        _LOGGER.info("No data available. While skip writing barchart: %s" % filename)
    # Set general plot properties
    # Plot 
    labels = (data[data.columns[0]].values)[0:25]
    y = (data[data.columns[1]].values)[0:25]
    fig, axs = plt.subplots(1, 1, figsize=(24, 10))
    labels_pos = np.arange(len(labels))
    axs.bar(labels_pos, y, color="green")
    # Labels
    plt.xticks(labels_pos, labels)
    axs.set_ylabel(ylabel)
    axs.set_title(title)
    for n, _y in enumerate(y):
        axs.annotate(
            s=str(_y),
            xy=(n, _y),
            ha='center',va='center',
            xytext=(0,10),
            textcoords='offset points',
            color="black"
        )
    # Optional - Make plot look nicer
    for label in axs.get_xticklabels():
        if len(label._text) > 60:
            label._text = "..."+label._text[-60:]
    plt.xticks(rotation=90)
    _writeFigure(fig, folder, filename)

def _writeFigure(figure, folder, filename):
    path = os.path.join(folder, filename)
    figure.savefig(path, bbox_inches='tight')
    plt.close(figure)
