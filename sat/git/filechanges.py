#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
from domain import Change
import git.changerepo as repo

import xls
import re
import plot
import pandas as pd
import os.path

_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")


class FileChanges(Analysis):

    @staticmethod
    def name():
        return "files"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._changes_per_file = []

    def load_data(self, workingdir, ignored_path_segments):
        self._workingDir = workingdir
        self._changes = repo.get_file_changes(workingdir, self._since)

    def analyse(self, ignoredPathSegments):
        if not self._changes:
            self._logger.warn("No changes found. No output will be written.")
            return
        filepaths = set([change.filepath for change in self._changes])
        for filepath in filepaths:
            lines_added = 0
            lines_removed = 0
            for change in self._changes:
                if change.filepath == filepath:
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            self._changes_per_file.append(
                Change(lines_added, lines_removed, filepath))
        # Filter for existing files
        #self.changesPerFile[:] = [change for change in self.changesPerFile if os.path.isfile(os.path.join(self._workingDir,change.filepath))]
        self._changes_per_file.sort(
            key=lambda c: c.lines_added+c.lines_removed, reverse=True)

    def write_results(self, outputdir):
        self._write_barchart(outputdir)
        self._write_report(outputdir)

    def _write_report(self, outputdir):
        rows = []
        rows.append(["File", "Lines changed", "Lines added", "Lines removed"])
        for change in self._changes_per_file:
            overall_changes = change.lines_added+change.lines_removed
            rows.append([change.filepath,
                         overall_changes, change.lines_added, change.lines_removed])
        filepath = os.path.join(outputdir, "changed_lines_per_file.xls")
        sheet_name = "Changes since "+self._since
        xls.write_xls(sheet_name, rows, filepath)

    def _write_barchart(self, outputDir):
        filepaths = [change.filepath for change in self._changes_per_file]
        data = []
        for change in self._changes_per_file[0:25]:
            data.append([change.lines_added, change.lines_removed])
        df = pd.DataFrame(data=data, index=filepaths[0:25], columns=[
                          "Added", "Removed"])
        if not df.empty:
            plot.plot_stacked_barchart(df, "Number of changed lines",
                                       "Number of changed lines for most changed files since "+self._since, outputDir, "most_changed_files.pdf")
