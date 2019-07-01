#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd

_CSV_SEPARATOR = "\t"
_LIST_SEPARATOR = ", "


def write_dataframe_to_xls(data, filename, outputdir, sheetname):
    filepath = os.path.join(outputdir, filename)
    writer = pd.ExcelWriter(filepath)
    data.to_excel(writer, sheetname, index=False)
    writer.save()


def write_graphml(path, graph):
    with open(path, "w") as output_file:
        output_file.write(graph.serialize())


def write_cycles_to_txt(path, cycles):
    with open(path, "w") as output_file:
        for cycle in cycles:
            cycle_list = _LIST_SEPARATOR.join(sorted(cycle))
            output_file.write(cycle_list + "\n")


def write_bundles_to_csv(path, bundles, header):
    with open(path, "w") as output_file:
        output_file.write(_CSV_SEPARATOR.join(header) + "\n")
        for bundle in sorted(
            sorted(bundles, key=lambda x: x.name),
            key=lambda x: x.num_dependencies,
            reverse=True,
        ):
            output_file.write(
                _CSV_SEPARATOR.join(
                    [
                        bundle.name,
                        bundle.version,
                        str(bundle.num_dependencies),
                        _LIST_SEPARATOR.join(bundle.exported_packages),
                        _LIST_SEPARATOR.join(bundle.imported_packages),
                        _LIST_SEPARATOR.join(bundle.required_bundles),
                        bundle.path,
                    ]
                )
                + "\n"
            )
