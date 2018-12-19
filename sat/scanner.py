#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import xml.etree.ElementTree

class Scanner:

    @staticmethod
    def find_projects(directory, ignored_path_segments):
        project_dirs = []
        for dirpath, dirnames, files in os.walk(directory):
            ignored = any(ignored_segment in dirpath for ignored_segment in ignored_path_segments)
            if not ignored: 
                for file in files:
                    if file == ".classpath": 
                        project_dirs.append(os.path.normpath(dirpath))
        return project_dirs

    @staticmethod
    def find_packages(directory, ignored_path_segments):
        project_dirs = Scanner.find_projects(directory, ignored_path_segments)
        relpaths_for_packagepaths = dict()
        for project_dir in project_dirs:
            sourcefolders_for_project = Scanner._find_sourcefolders_for_project(project_dir)
            for sourcefolder in sourcefolders_for_project:
                packages_for_project = Scanner._find_sourcepackages_for_sourcefolder(sourcefolder)
                for package_for_project in packages_for_project:
                    relpath = os.path.normpath(os.path.relpath(package_for_project, sourcefolder))
                    relpaths_for_packagepaths[package_for_project] = relpath
        return relpaths_for_packagepaths

    @staticmethod
    def _find_sourcepackages_for_sourcefolder(sourcefolder):
        sourcepackage_paths = []
        for dirpath, dirname, files in os.walk(sourcefolder):
            java_filenames = [file for file in files if file.endswith(".java")]
            if java_filenames:
                sourcepackage_path = os.path.normpath(dirpath)    
                sourcepackage_paths.append(sourcepackage_path)        
        return sourcepackage_paths

    @staticmethod
    def _find_sourcefolders_for_project(project_dir):
        classpathFilePath = os.path.join(project_dir,".classpath")
        relative_sourcefolders = Scanner._parse_classpath(classpathFilePath)
        sourcefolders = [os.path.normpath(os.path.join(project_dir, folder)) for folder in relative_sourcefolders]
        return sourcefolders

    @staticmethod
    def _parse_classpath(classpath_file_path):
        sourcefolders = []
        root = xml.etree.ElementTree.parse(classpath_file_path).getroot()
        for classpath in root.findall('classpathentry'):
            if classpath.get('kind') == "src":
                sourcefolders.append(classpath.get('path'))
        return sourcefolders    