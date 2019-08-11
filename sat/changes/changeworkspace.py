#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sat.app.workspace.workspace import Workspace
from sat.changes.domain import Project, Package, SourceFile
import sat.changes.changeparser as parser


class ChangeWorkspace(Workspace):
    def __init__(self, directory, ignored_path_segments, since):
        super().__init__(directory, ignored_path_segments)
        self._changes_by_path = parser.parse_changes(directory, since)
        self.since = since

    def create_project(self, path, name):
        w_project = super().create_project(path, name)
        return Project(
            w_project.abs_path, w_project.rel_path, w_project.name, w_project.packages
        )

    def create_package(self, abs_path, rel_path):
        w_package = super().create_package(abs_path, rel_path)
        return Package(
            w_package.abs_path,
            w_package.rel_path,
            w_package.name,
            w_package.sourcefiles,
        )

    def create_sourcefile(self, java_file_path, abs_dir, packagename=""):
        w_sourcefile = super().create_sourcefile(java_file_path, abs_dir, packagename)
        change = self._changes_by_path[java_file_path]
        return SourceFile(
            w_sourcefile.abs_path, w_sourcefile.rel_path, w_sourcefile.name, change
        )
