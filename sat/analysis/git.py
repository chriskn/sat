#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
from domain import Change

import subprocess
import re
import plot
import pandas as pd
import os.path

_LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")

class GitChanges(Analysis):
    
    _changes = []
    _changes_per_file = []

    @staticmethod
    def name():
        return "gitChanges"

    def load_data(self, workingDir, ignoredPathSegments):
        self._workingDir = workingDir
        result = subprocess.run('git log --numstat --oneline --shortstat --after="2017-26-09" -- ' +
                                workingDir, stdout=subprocess.PIPE, cwd=workingDir, shell=True)
        lines = result.stdout.splitlines()
        for line in lines:
            decoded = line.decode('utf-8')
            if _LINES_CHANGED_PATTERN.match(decoded):
                split = decoded.split("\t")
                self._changes.append(
                    Change(int(split[0]), int(split[1]), split[2]))

    def analyse(self, ignoredPathSegments):
        filenames = set([change.filename for change in self._changes])
        for filename in filenames:
            lines_added = 0
            lines_removed = 0
            for change in self._changes:
                if change.filename == filename:
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            self._changes_per_file.append(
                Change(lines_added, lines_removed, filename))
        # Filter for existing files
        #self.changesPerFile[:] = [change for change in self.changesPerFile if os.path.isfile(os.path.join(self._workingDir,change.fileName))]
        self._changes_per_file.sort(
            key=lambda c: c.lines_added+c.lines_removed, reverse=True)

    def write_results(self, outputDir):
        filenames = [change.filename for change in self._changes_per_file]
        data = []
        for change in self._changes_per_file[0:25]:
            data.append([change.lines_added, change.lines_removed])
        df = pd.DataFrame(data=data, index=filenames[0:25], columns=[
                          "Added", "Removed"])
        plot.plot_stacked_barchart(df, "Number of changed lines",
                                 "Number of changed lines for most changed files", outputDir, "most_changed_files.pdf")
