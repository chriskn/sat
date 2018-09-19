#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re
from project.project import Project
from package.packageparser import PackageParser

import xml.etree.ElementTree


class ProjectParser:

    def __init__(self, directory, ignoredPathSegments):
        self.directory = directory
        self.ignoredPathSegments = ignoredPathSegments
        self.packageParser = PackageParser()

    def parseProjects(self):
        projetcPaths = self._scanForProjects()
        projects = [self._parseProject(projectPath) for projectPath in projetcPaths]
        return projects

    def _scanForProjects(self):
        projects = []
        for dirpath, dirNames, files in os.walk(self.directory):
            ignored = any(ignoredSegment in dirpath for ignoredSegment in self.ignoredPathSegments)
            if not ignored: 
                for file in files:
                    if file == ".classpath": 
                        projects.append(dirpath)
        return projects

    def _parseProject(self, projectPath):
        classpathFilePath = os.path.join(projectPath,".classpath")
        relativeSourceFolders = self._parseClasspath(classpathFilePath)
        sourceFolders = [os.path.join(projectPath, s) for s in relativeSourceFolders]
        javaSourcePackages = self.packageParser.parsePackages(sourceFolders)
        project = Project(os.path.basename(projectPath), projectPath, javaSourcePackages)
        return project

    def _parseClasspath(self, classpathFilePath):
        sourceFolders = []
        root = xml.etree.ElementTree.parse(classpathFilePath).getroot()
        for classpath in root.findall('classpathentry'):
            if classpath.get('kind') == "src":
                sourceFolders.append(classpath.get('path'))
        return sourceFolders

