#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import squarify

sns.set()

_DPI = 72.27
_LOGGER = logging.getLogger(__name__)
_MAX_HEATMAP_ENTRIES = 200
_MAX_TREEMAP_ENTRIES = 25


def plot_heatmap(data_frame, title, folder, file_name):
    number_of_entries = data_frame.shape[0]
    if number_of_entries > _MAX_HEATMAP_ENTRIES:
        _LOGGER.warning(
            "Number of entries is %d and exceeds limit of %d for heatmaps. Will skip creation of heatmap",
            number_of_entries,
            _MAX_HEATMAP_ENTRIES,
        )
        return
    fontsize_pt = plt.rcParams["ytick.labelsize"]
    # compute the required figure height
    matrix_height_pt = fontsize_pt * number_of_entries * 1.02
    matrix_height_in = matrix_height_pt / _DPI
    entry_offset = number_of_entries * 0.2
    figure_size = int(round(matrix_height_in + entry_offset))
    # colors
    color_map = plt.get_cmap("autumn_r", 10)
    # build figure
    fig, axis = plt.subplots(figsize=(figure_size, figure_size))
    axis.set_title(title)
    # plot
    sns.heatmap(
        data_frame,
        square=True,
        fmt="d",
        ax=axis,
        xticklabels=True,
        yticklabels=True,
        annot_kws={"size": 8},
        annot=True,
        cbar_kws={"shrink": 0.5},
        cmap=color_map,
        linewidths=0.5,
        linecolor="grey",
    )
    _write_figure(fig, folder, file_name)


def plot_scatterplot(data, folder, file_name):
    sns.set_context({"figure.figsize": (24, 10)})
    cmap = sns.cubehelix_palette(dark=0.3, light=0.8, as_cmap=True)
    axes = sns.scatterplot(
        x="INSTRUCTION_MISSED",
        y="INSTRUCTION_COVERED",
        hue="COMPLEXITY_MISSED",
        size="COMPLEXITY_MISSED",
        palette=cmap,
        data=data,
    )
    for line in range(0, data.shape[0]):
        axes.text(
            data.INSTRUCTION_MISSED[line] + 0.2,
            data.INSTRUCTION_COVERED[line] + 0.05,
            data.CLASS[line],
            horizontalalignment="left",
            size="medium",
            color="black",
            weight="semibold",
        )
    # plt.show()
    _write_figure(axes.get_figure(), folder, file_name)


def plot_treemap(data, title, folder, file_name, value_name):
    # pylint: disable=R0914
    if data.empty:
        _LOGGER.info("No data available. Skip writing stacked barchart: %s", file_name)
        return
    number_of_entries = data.shape[0]
    # restrict number of values
    if number_of_entries > _MAX_TREEMAP_ENTRIES:
        _LOGGER.warning(
            "Number of entries  (%d) exceeds limit for treemaps. Will limit to max %d values",
            len(data),
            _MAX_TREEMAP_ENTRIES,
        )
    values = data[data.columns[1]].values
    names = data[data.columns[0]].values
    labels = []
    for index, name in enumerate(names):
        label = name
        if len(name) > 30:
            label = _wrap_label(name, 25)
        label = "\n".join([label, value_name + " " + "%.2f" % round(values[index], 2)])
        labels.append(label)
    # the sum of the values must equal the total area to be laid out
    # i.e., sum(values) == width * height
    norm_values = squarify.normalize_sizes(values, 700.0, 433.0)
    # colors
    color_map = plt.get_cmap("autumn_r", len(labels))
    colors = [color_map(i) for i in range(len(norm_values))][::-1]
    # plot
    plt.rc("font", size=8)
    fig = plt.figure(figsize=(12, 10))
    axis = fig.add_subplot(111)
    axis = squarify.plot(
        sizes=norm_values, color=colors, label=labels, ax=axis, alpha=0.7
    )
    axis.set_xticks([])
    axis.set_yticks([])
    axis.set_title(title, fontsize=16)
    # color bar
    img_data = np.array(values)
    img_data = np.expand_dims(img_data, axis=0)
    img = plt.imshow(img_data, cmap=color_map)
    img.set_visible(False)
    fig.colorbar(img, orientation="vertical", shrink=0.96)
    _write_figure(plt.gcf(), folder, file_name)


def plot_stacked_barchart(data, ylabel, title, folder, file_name):
    if data.empty:
        _LOGGER.info("No data available. Skip writing stacked barchart: %s", file_name)
        return
    data_column_1 = data.columns[1]
    data_column_2 = data.columns[2]
    column_data_1 = data[data_column_1].values
    column_data_2 = data[data_column_2].values
    total = column_data_1 + column_data_2
    # Set general plot properties
    sns.set_style("white")
    sns.set_context({"figure.figsize": (24, 10)})
    labels = _trim_labels(data[data.columns[0]].values, 40)
    # Plot 1 - background - "total" (top) series
    sns.barplot(x=labels, y=total, color="red")
    # Plot 2 - overlay - "bottom" series
    bottom_plot = sns.barplot(x=labels, y=column_data_1, color="green")
    # Legend
    top_bar = plt.Rectangle((0, 0), 1, 1, fc="red", edgecolor="none")
    bottom_bar = plt.Rectangle((0, 0), 1, 1, fc="green", edgecolor="none")
    legend = plt.legend(
        [bottom_bar, top_bar],
        [data_column_1, data_column_2],
        loc=1,
        ncol=2,
        prop={"size": 16},
    )
    legend.draw_frame(False)
    bottom_plot.set_ylabel(ylabel)
    bottom_plot.set_title(title)
    # remove spines
    sns.despine(left=True)
    # rotate labels
    bottom_plot.set_xticklabels(bottom_plot.get_xticklabels(), rotation=80)
    _write_figure(bottom_plot.get_figure(), folder, file_name)


def plot_barchart(data, ylabel, title, folder, filename):
    if data.empty:
        _LOGGER.info("No data available. While skip writing barchart: %s", filename)
        return
    # Plot
    y_values = (data[data.columns[1]].values)[0:25]
    fig, axis = plt.subplots(1, 1, figsize=(24, 10))
    # Labels
    labels = _trim_labels((data[data.columns[0]].values)[0:25], 60)
    labels_pos = np.arange(len(labels))
    axis.bar(labels_pos, y_values, color="green")
    plt.xticks(labels_pos, labels)
    axis.set_ylabel(ylabel)
    axis.set_title(title)
    for index, y_value in enumerate(y_values):
        axis.annotate(
            s=str(y_value),
            xy=(index, y_value),
            ha="center",
            va="center",
            xytext=(0, 10),
            textcoords="offset points",
            color="black",
        )
    plt.xticks(rotation=90)
    _write_figure(fig, folder, filename)


def _trim_labels(orig_labels, max_length):
    labels = []
    for label in orig_labels:
        if len(label) > max_length:
            label = "..." + label[-max_length:]
        labels.append(label)
    return labels


def _wrap_label(label, length):
    labellines = []
    offset = 5
    towrap = label
    while len(towrap) > length + offset:
        left, right = towrap[:length], towrap[length:]
        labellines.extend([left, right])
        towrap = right
    return "\n".join(labellines)


def _write_figure(figure, folder, filename):
    path = os.path.join(folder, filename)
    figure.savefig(path, bbox_inches="tight")
    plt.close(figure)
