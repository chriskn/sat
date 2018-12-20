#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
from domain import Change

import xlwt
import re
import plot
import pandas as pd
import os.path
from scanner import Scanner
import git.changerepo as repo
from collections import OrderedDict


_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")


class PackageChanges(Analysis):

    @staticmethod
    def name():
        return "gitpackages"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._changes_per_package = []

    def load_data(self, workingdir, ignored_path_segments):
        self._workingDir = workingdir
        self._changes = repo.get_file_changes(workingdir, self._since)

    def analyse(self, ignored_path_segments):
        relativepaths_for_package_paths = Scanner.find_packages(
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
                if relative_package_path in file_directory:
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
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Lines_changed_since_"+self._since)
        self._write_row(ws, 0, ["Package", "Lines changed", "Lines added", "Lines removed"])
        column=1
        for change in self._changes_per_package:
            overall_changes = change.lines_added+change.lines_removed
            row_data = [change.filepath.replace("\\", "."),
                     overall_changes, change.lines_added, change.lines_removed]
            self._write_row(ws, column, row_data)
            column+=1
        wb.save(os.path.join(outputdir, "changed_lines_per_package.xls"))

    def _write_row(self, sheet, rindex, data):
        i = 0
        for d in data: 
            sheet.write(rindex, i, str(d))
            i+=1

    def _write_treemap(self, outputdir):
        data = OrderedDict()
        for change in self._changes_per_package:
            label = change.filepath.replace("\\", ".")
            num_changes = change.lines_added+change.lines_removed
            data[label] = int(num_changes)
        if data:
            plot.plot_treemap(data, "Number of changed lines per packag since " +
                              self._since, outputdir, "changed_lines_per_package.pdf")
