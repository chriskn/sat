#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
from changes.domain import Change

import xls
import re
import plot
import pandas as pd
import os.path
import scanner
import changes.changerepo as repo
from collections import OrderedDict



class ProjectChanges(Analysis):

    @staticmethod
    def name():
        return "projects"

    def __init__(self, since):
        self._since = since
        self._changes = []
        self._changes_per_project = []

    def load_data(self, workingdir, ignored_path_segments):
        self._workingDir = os.path.normpath(workingdir)
        self._changes = repo.changes(workingdir, self._since)

    def analyse(self, ignored_path_segments):
        self._logger.info("Analysing project changes.")
        project_paths = scanner.find_projects(
            self._workingDir, ignored_path_segments)
        if not project_paths:
            self._logger.warn("No projects found. No output will be written.")
            return
        if not self._changes:
            self._logger.warn("No changes found. No output will be written.")
            return
        for project_path in project_paths:
            lines_added = 0
            lines_removed = 0
            for change in self._changes:
                file_directory = os.path.normpath(
                    os.path.dirname(change.path))
                rel_proj_path =  project_path.replace(self._workingDir, "")
                if rel_proj_path.startswith("\\"):
                    rel_proj_path = rel_proj_path[1:]
                if rel_proj_path in file_directory:
                    lines_added += change.lines_added
                    lines_removed += change.lines_removed
            if lines_added+lines_removed > 0:
                self._changes_per_project.append(
                    Change(project_path, lines_added, lines_removed))
        self._changes_per_project.sort(
            key=lambda c: c.lines_added+c.lines_removed, reverse=True)

    def write_results(self, outputdir):
        self._write_report(outputdir)
        self.write_treemap(outputdir)

    def _write_report(self, outputdir):
        rows = []
        rows.append(["Project", "Lines changed",
                     "Lines added", "Lines removed"])
        for change in self._changes_per_project:
            overall_changes = change.lines_added+change.lines_removed
            project_name = os.path.basename(change.path)
            rows.append([project_name,
                         overall_changes, change.lines_added, change.lines_removed])
        filepath = os.path.join(outputdir, "changed_lines_per_project.xls")
        sheet_name = "Changes since "+self._since
        xls.write_xls(sheet_name, rows, filepath)

    def write_treemap(self, outputdir):
        data = []
        for change in self._changes_per_project:
            label = os.path.basename(change.path)
            data.append((label, change.total_lines))
        if data:
            df = pd.DataFrame(data=data, columns=["Projects", "Changes"])
            plot.plot_treemap(df, "Number of changed lines per project since " +
                              self._since, outputdir, "changed_lines_per_project.pdf", "changes:")
