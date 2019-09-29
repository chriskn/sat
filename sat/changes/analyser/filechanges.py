#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ntpath

import pandas as pd
import os
import sat.app.report.plot as plot
import sat.app.report.writer as writer

from sat.app.execution.analyser import Analyser


class FileChanges(Analyser):

    _COLUMNS = [
        "Path",
        "File",
        "Number of lines",
        "Changed Lines",
        "Lines added",
        "Lines removed",
        "Number of contributers",
        "Number of contributions",
        "Number of fixes",
    ]

    @staticmethod
    def name():
        return "files"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._sourcefiles = []
        self._analysis_result = None

    def load_data(self):
        self._sourcefiles = self._workspace.sourcefiles()

    def analyse(self):
        self._logger.info("Analysing file changes.")
        data = [
            (
                sourcefile.abs_path,
                sourcefile.name,
                sum(1 for line in open(sourcefile.abs_path)),
                sourcefile.changes_total,
                sourcefile.lines_added,
                sourcefile.lines_removed,
                sourcefile.num_contributer,
                len(sourcefile.changes),
                sourcefile.num_fixes,
            )
            for sourcefile in self._sourcefiles
            if sourcefile.changes_total > 0 and os.path.isfile(sourcefile.abs_path)
        ]
        dataframe = pd.DataFrame(data=data, columns=FileChanges._COLUMNS)
        self._analysis_result = dataframe.sort_values(
            FileChanges._COLUMNS[3], ascending=False
        )
        return self._analysis_result

    def write_results(self, output_dir):
        writer.write_dataframe_to_xls(
            self._analysis_result,
            "changed_lines_per_file.xls",
            output_dir,
            "Changes since " + self._workspace.since,
        )
        writer.write_dataframe_to_csv(
            self._analysis_result, "changed_lines_per_file.csv", output_dir
        )
        barchart_data = self._create_barchart_data()
        plot.plot_stacked_barchart(
            barchart_data,
            "Number of changed lines",
            "Number of changed lines for most changed files since "
            + self._workspace.since,
            output_dir,
            "most_changed_files.pdf",
        )

    def _create_barchart_data(self):
        columns_to_drop = [FileChanges._COLUMNS[1], FileChanges._COLUMNS[2]]
        barchart_data = self._analysis_result.iloc[0:25].drop(columns=columns_to_drop)
        return barchart_data


def _file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
