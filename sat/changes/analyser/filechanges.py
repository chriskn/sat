#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ntpath

import pandas as pd

import changes.changerepo as repo
import report.plot as plot
import report.xls as xls
from app.analyser import Analyser


class FileChanges(Analyser):

    _COLUMNS = ["Path", "File", "Total changes",
                "Lines added", "Lines removed"]

    @staticmethod
    def name():
        return "files"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._changes_per_file = []
        self._working_dir = None
        self._analysis_result = None

    def load_data(self, working_dir, ignored_path_segments):
        self._working_dir = working_dir
        self._changes = repo.changes(working_dir, self._since)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing file changes.")
        data = []
        filepaths = {change.path for change in self._changes}
        for filepath in filepaths:
            file_name = _file_name(filepath)
            lines_added = 0
            lines_removed = 0
            for change in self._changes:
                if change.path == filepath:
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            data.append((filepath, file_name, lines_added +
                         lines_removed, lines_added, lines_removed))
        dataframe = pd.DataFrame(data=data, columns=FileChanges._COLUMNS)
        self._analysis_result = dataframe.sort_values(FileChanges._COLUMNS[2], ascending=False)
        return self._analysis_result

    def write_results(self, output_dir):
        xls.write_data_frame(self._analysis_result, "changed_lines_per_file.xls",
                             output_dir, "Changes since " + self._since)
        barchart_data = self._create_barchart_data()
        plot.plot_stacked_barchart(
            barchart_data,
            "Number of changed lines",
            "Number of changed lines for most changed files since " +
            self._since,
            output_dir,
            "most_changed_files.pdf")

    def _create_barchart_data(self):
        columns_to_drop = [FileChanges._COLUMNS[1], FileChanges._COLUMNS[2]]
        barchart_data = self._analysis_result.iloc[0:25].drop(columns=columns_to_drop)
        return barchart_data


def _file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
