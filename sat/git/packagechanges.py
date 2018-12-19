#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
from domain import Change

import re
import plot
import pandas as pd
import os.path
from scanner import Scanner
import git.changerepo as repo

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
        for fullpath, relative_path in relativepaths_for_package_paths.items():
            lines_added = 0
            lines_removed = 0
            for change in self._changes:
                dir = os.path.normpath(os.path.dirname(change.filepath))
                if dir in fullpath:
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            if lines_added+lines_removed > 0:
                self._changes_per_package.append(
                    Change(lines_added, lines_removed, relative_path))
        self._changes_per_package.sort(
            key=lambda c: c.lines_added+c.lines_removed, reverse=True)

    def write_results(self, outputDir):
        labels = [change.filepath.replace("\\", ".")
                  for change in self._changes_per_package]
        changes = [change.lines_added +
                   change.lines_removed for change in self._changes_per_package]
        if labels:
            plot.plot_treemap(labels, changes, "Number of changed lines per packag since " +
                              self._since, outputDir, "changed_lines_per_package.pdf")
