#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re
from deps.domain import Project
from deps.parser.packageparser import PackageParser

import xml.etree.ElementTree


class ProjectParser:

    def __init__(self, directory, ignoredPathSegments):
        self.directory = directory
        self.ignored_path_segments = ignoredPathSegments
        self.package_parser = PackageParser()

    def parse(self):
        projetc_paths = self._scan()
        projects = [self._parseProject(projectPath) for projectPath in projetc_paths]
        return projects

    def _scan(self):
        projects = []
        for dirpath, dirnames, files in os.walk(self.directory):
            ignored = any(ignored_segment in dirpath for ignored_segment in self.ignored_path_segments)
            if not ignored: 
                for file in files:
                    if file == ".classpath": 
                        projects.append(dirpath)
        return projects

    def _parseProject(self, project_path):
        classpathFilePath = os.path.join(project_path,".classpath")
        relative_sourcefolders = self._parse_classpath(classpathFilePath)
        sourcefolders = [os.path.join(project_path, s) for s in relative_sourcefolders]
        java_source_packages = self.package_parser.parse_packages(sourcefolders)
        project = Project(os.path.basename(project_path), project_path, java_source_packages)
        return project

    def _parse_classpath(self, classpath_file_path):
        sourcefolders = []
        root = xml.etree.ElementTree.parse(classpath_file_path).getroot()
        for classpath in root.findall('classpathentry'):
            if classpath.get('kind') == "src":
                sourcefolders.append(classpath.get('path'))
        return sourcefolders

