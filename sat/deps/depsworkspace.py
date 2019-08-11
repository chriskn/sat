#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sat.app.workspace.workspace import Workspace
from sat.deps.domain import Project, Package
import sat.deps.ast_deps_parser as source_parser


class DepsWorkspace(Workspace):
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
        source_file = source_parser.parse_java_sourcefile(w_sourcefile)
        return source_file
