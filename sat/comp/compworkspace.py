#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sat.app.workspace.workspace import Workspace
from sat.comp.domain import Project, Package, SourceFile
import sat.comp.parser.typeparser as tparser


class CompWorkspace(Workspace):
    def __init__(self, workspace_dir, ignored_path_segments):
        super().__init__(workspace_dir, ignored_path_segments)
        self.types = dict()

    def create_project(self, path, name):
        w_project = super().create_project(path, name)
        return Project(
            w_project.abs_path, w_project.rel_path, w_project.name, w_project.packages
        )

    def create_package(self, abs_path, rel_path, proj_name):
        w_package = super().create_package(abs_path, rel_path, proj_name)
        return Package(
            w_package.abs_path,
            w_package.rel_path,
            w_package.name,
            w_package.sourcefiles,
            w_package.proj_name,
        )

    def create_sourcefile(self, java_file_path, abs_dir, packagename=""):
        w_sourcefile = super().create_sourcefile(java_file_path, abs_dir, packagename)
        types = tparser.parse(w_sourcefile)
        return SourceFile(
            w_sourcefile.abs_path, w_sourcefile.rel_path, w_sourcefile.name, types
        )
