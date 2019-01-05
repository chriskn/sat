#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
from git.domain import Change

import xls
import re
import plot
import pandas as pd
import os.path
import scanner
import git.changerepo as repo
from collections import OrderedDict

_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")

class PackageChanges(Analysis):

    @staticmethod
    def name():
        return "packages"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._changes_per_package = []

    def load_data(self, workingdir, ignored_path_segments):
        self._workingDir = workingdir
        self._changes = repo.get_file_changes(workingdir, self._since)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing package changes.")
        relativepaths_for_package_paths = scanner.find_packages(
            self._workingDir, ignored_path_segments)
        if not relativepaths_for_package_paths:
            self._logger.warn("No packages found. No output will be written.")
            return
        if not self._changes:
            self._logger.warn("No changes found. No output will be written.")
            return
        for fullpath, relative_package_path in relativepaths_for_package_paths.items():
            lines_added = 0
            lines_removed = 0
            for change in self._changes:
                file_directory = os.path.normpath(
                    os.path.dirname(change.filepath))
                if  file_directory.endswith(relative_package_path):
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            if lines_added+lines_removed > 0:
                self._changes_per_package.append(
                    Change(lines_added, lines_removed, relative_package_path))
        self._changes_per_package.sort(
            key=lambda c: c.lines_added+c.lines_removed, reverse=True)

    def write_results(self, outputdir):
        self._write_report(outputdir)
        self._write_treemap(outputdir)

    def _write_report(self, outputdir):
        rows = []
        rows.append(["Package", "Lines changed", "Lines added", "Lines removed"])
        for change in self._changes_per_package:
            overall_changes = change.lines_added+change.lines_removed
            rows.append([change.filepath.replace("\\", "."),
                     overall_changes, change.lines_added, change.lines_removed])
        filepath = os.path.join(outputdir, "changed_lines_per_package.xls")
        sheet_name = "Changes since "+self._since
        xls.write_xls(sheet_name, rows, filepath)

    def _write_treemap(self, outputdir):
        data = []
        for change in self._changes_per_package:
            label = change.filepath.replace("\\", ".")
            num_changes = change.lines_added+change.lines_removed
            data.append((label, int(num_changes)))
        if data:
            df = pd.DataFrame(data=data, columns=["Package", "Changes"])
            plot.plot_treemap(df, "Number of changed lines per packag since " +
                              self._since, outputdir, "changed_lines_per_package.pdf", "changes:")
