#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

from sat.app.execution.analyser import Analyser

import sat.app.report.plot as plot
import sat.app.report.writer as writer


class PackageChanges(Analyser):

    _COLUMNS = [
        "Path",
        "Package",
        "Total changes",
        "Lines added",
        "Lines removed",
        "Number of contributers",
    ]

    @staticmethod
    def name():
        return "packages"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._analysis_result = None
        self._packages = []

    def load_data(self):
        self._packages = self._workspace.packages()

    def analyse(self):
        self._logger.info("Analysing package changes.")
        data = [
            (
                package.abs_path,
                package.name,
                package.changes_total,
                package.lines_added,
                package.lines_removed,
                package.num_contributer,
            )
            for package in self._packages
            if package.changes_total > 0
        ]
        dataframe = pd.DataFrame(data=data, columns=PackageChanges._COLUMNS)
        self._analysis_result = dataframe.sort_values(
            PackageChanges._COLUMNS[2], ascending=False
        )
        return self._analysis_result

    def write_results(self, output_dir):
        writer.write_dataframe_to_xls(
            self._analysis_result,
            "changed_lines_per_package.xls",
            output_dir,
            "Changes since " + self._workspace.since,
        )
        tm_data = self._create_tm_data()
        plot.plot_treemap(
            tm_data,
            "Number of changed lines per packag since " + self._workspace.since,
            output_dir,
            "changed_lines_per_package.pdf",
            "changes:",
        )

    def _create_tm_data(self):
        tm_data = self._analysis_result.drop(
            columns=["Path", "Lines added", "Lines removed"]
        )
        return tm_data[tm_data[PackageChanges._COLUMNS[2]] > 0]
