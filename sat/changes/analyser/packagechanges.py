#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

import pandas as pd

import changes.changerepo as repo
import scanner
from app.analyser import Analyser

import report.plot as plot
import report.xls as xls


class PackageChanges(Analyser):

    _COLUMNS = ["Path", "Package", "Lines changed", "Lines added", "Lines removed"]

    @staticmethod
    def name():
        return "packages"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._analysis_result = None
        self._workingdir = None
        self._relativepaths_for_package_paths = None

    def load_data(self, workingdir, ignored_path_segments):
        self._workingdir = workingdir
        self._changes = repo.changes(workingdir, self._since)
        self._relativepaths_for_package_paths = scanner.find_packages(
            self._workingdir, ignored_path_segments)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing package changes.")
        data = []
        for full_package_path, relative_package_path in self._relativepaths_for_package_paths.items():
            lines_added = 0
            lines_removed = 0
            name = relative_package_path.replace(os.sep, ".")
            for change in self._changes:
                change_directory = os.path.normpath(os.path.dirname(change.path))
                norm_package_path = self._norm_path(full_package_path)
                if change_directory.endswith(norm_package_path):
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            data.append((relative_package_path, name, lines_added+lines_removed, lines_added, lines_removed))
        dataframe = pd.DataFrame(data=data, columns=PackageChanges._COLUMNS)
        self._analysis_result = dataframe.sort_values(PackageChanges._COLUMNS[2], ascending=False)
        return self._analysis_result

    def _norm_path(self, full_package_path):
        norm_package_path = full_package_path.replace(self._workingdir, "")
        rel_pattern = "[.]+"+re.escape(os.sep)
        if re.match(rel_pattern, norm_package_path):
            norm_package_path = re.sub(rel_pattern, '', norm_package_path)
        return norm_package_path

    def write_results(self, outputfolder):
        xls.write_data_frame(self._analysis_result, "changed_lines_per_package.xls",
                             outputfolder, "Changes since "+self._since)
        tm_data = self._create_tm_data()
        plot.plot_treemap(tm_data, "Number of changed lines per packag since " +
                          self._since, outputfolder, "changed_lines_per_package.pdf", "changes:")

    def _create_tm_data(self):
        tm_data = self._analysis_result.drop(columns=["Path", "Lines added", "Lines removed"])
        return tm_data[tm_data[PackageChanges._COLUMNS[2]] > 0]
