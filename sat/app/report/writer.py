#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd

_LIST_SEPARATOR = ", "


def write_dataframe_to_xls(data, filename, outputdir, sheetname):
    filepath = os.path.join(outputdir, filename)
    writer = pd.ExcelWriter(filepath)
    data.to_excel(writer, sheetname, index=False)
    writer.save()


def write_dataframe_to_csv(data, filename, outputdir):
    filepath = os.path.join(outputdir, filename)
    data.to_csv(filepath, index=False, sep=";", decimal=",")


def write_graphml(path, graph):
    with open(path, "w") as output_file:
        output_file.write(graph.serialize())


def write_cycles_to_txt(path, cycles):
    with open(path, "w") as output_file:
        for cycle in cycles:
            cycle_list = _LIST_SEPARATOR.join(sorted(cycle))
            output_file.write(cycle_list + "\n")
