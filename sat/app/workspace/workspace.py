#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sat.app.workspace.scanner as scanner
from sat.app.workspace.domain import Project, Package, SourceFile, Bundle
import sat.app.workspace.parser.java_parser as java
import sat.app.workspace.parser.manifest_parser as manifestparser
import logging


class Workspace:
    def __init__(self, workspace_dir, ignored_path_segments):
        self.workspace_dir = os.path.abspath(os.path.normpath(workspace_dir))
        self.ignored_path_segments = ignored_path_segments
        self._projects = dict()
        self._packages = dict()
        self._sourcefiles = dict()
        self.logger = logging.getLogger(Workspace.__name__)

    def projects(self):
        abs_dir = os.path.abspath(os.path.normpath(self.workspace_dir))
        parsed_projects = self._projects.get(abs_dir)
        if parsed_projects:
            return parsed_projects
        project_paths = scanner.find_projects(
            self.workspace_dir, self.ignored_path_segments
        )
        self.logger.info("Parsing %d projects", len(project_paths))
        projects = [
            self.create_project(path, name) for path, name in project_paths.items()
        ]
        return projects

    def bundles(self):
        bundle_paths = scanner.find_bundles(
            self.workspace_dir, self.ignored_path_segments
        )
        self.logger.info("Parsing %d bundles", len(bundle_paths))
        bundles = sorted(
            [self.create_bundle(bundle_path) for bundle_path in bundle_paths]
        )
        return bundles

    def packages(self, sourcefolder=None, proj_name=""):
        directory = sourcefolder if sourcefolder else self.workspace_dir
        abs_dir = os.path.abspath(os.path.normpath(directory))
        packages = []
        if sourcefolder:
            package_paths = scanner.find_packages_for_sourcefolder(
                abs_dir, self.ignored_path_segments
            )
            for path in package_paths:
                if path in self._packages:
                    packages.append(self._packages[path])
                else:
                    new_package = self.create_package(
                        path, os.path.relpath(os.path.abspath(path), abs_dir), proj_name
                    )
                    packages.append(new_package)
                    self._packages[path] = new_package
            self._packages[abs_dir] = packages
            return packages
        rel_path_for_abs_path = scanner.find_packages(
            self.workspace_dir, self.ignored_path_segments
        )
        for abs_path, rel_path in rel_path_for_abs_path.items():
            if abs_path in self._packages:
                packages.append(self._packages[abs_path])
            else:
                new_package = self.create_package(abs_path, rel_path, proj_name)
                self._packages[abs_path] = new_package
                packages.append(new_package)
        return packages

    def sourcefiles(self, directory=None, packagename=""):
        abs_dir = directory if directory else self.workspace_dir
        parsed_sourcefiles = self._sourcefiles.get(abs_dir)
        if parsed_sourcefiles:
            return parsed_sourcefiles
        java_file_paths = scanner.find_sourcefiles(abs_dir, self.ignored_path_segments)
        sourcefiles = [
            self.create_sourcefile(java_file_path, abs_dir, packagename)
            for java_file_path in java_file_paths
        ]
        return sourcefiles

    def create_project(self, path, name):
        abs_proj_path = os.path.abspath(path)
        rel_proj_path = os.path.relpath(abs_proj_path, self.workspace_dir)
        sourcefolders = scanner.find_sourcefolders_for_project(abs_proj_path)
        packages = []
        for sourcefolder in sourcefolders:
            packages.extend(self.packages(sourcefolder, name))
        return Project(abs_proj_path, rel_proj_path, name, packages)

    def create_package(self, abs_path, rel_path, proj_name=""):
        name = rel_path.replace(os.sep, ".")
        sourcefiles = self.sourcefiles(abs_path, name)
        return Package(abs_path, rel_path, name, sourcefiles, proj_name)

    def create_sourcefile(self, java_file_path, abs_dir, packagename="", parse=True):
        # pylint:disable=R0201
        abs_source_path = os.path.abspath(java_file_path)
        rel_source_path = os.path.relpath(abs_source_path, abs_dir)
        filename = os.path.basename(abs_source_path)
        ast = None
        if parse:
            ast = java.parse(abs_source_path)
        return SourceFile(abs_source_path, rel_source_path, filename, ast, packagename)

    def create_bundle(self, bundle_path):
        abs_bundle_path = os.path.abspath(bundle_path)
        rel_bundle_path = os.path.relpath(abs_bundle_path, self.workspace_dir)
        manifest_path = os.path.join(bundle_path, "META-INF", "MANIFEST.MF")
        symbolic_name, version, exported_packages, imported_packages, required_bundles = manifestparser.parse_manifest(
            manifest_path
        )
        number_of_dependencies = len(required_bundles) + len(imported_packages)
        bundle = Bundle(
            abs_bundle_path,
            rel_bundle_path,
            symbolic_name,
            version,
            exported_packages,
            imported_packages,
            required_bundles,
            number_of_dependencies,
        )
        return bundle
