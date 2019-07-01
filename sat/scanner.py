#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree
import itertools


def find_projects(directory, ignored_path_segments):
    project_dirs = dict()
    for dirpath, _, files in os.walk(directory):
        for file in files:
            if file == ".classpath":
                path = os.path.normpath(dirpath)
                ignored = any(
                    ignored_segment in path for ignored_segment in ignored_path_segments
                )
                if not ignored:
                    name = path.split(os.sep)[-1]
                    project_dirs[path] = name
    return project_dirs


def find_packages(directory, ignored_path_segments):
    project_dirs = find_projects(directory, ignored_path_segments)
    relpaths_for_packagepaths = dict()
    for project_dir in project_dirs:
        sourcefolders_for_project = _find_sourcefolders_for_project(project_dir)
        for sourcefolder in sourcefolders_for_project:
            packages_for_project = _find_sourcepackages_for_sourcefolder(sourcefolder)
            for package_for_project in packages_for_project:
                ignored = any(
                    ignored_segment in package_for_project
                    for ignored_segment in ignored_path_segments
                )
                if not ignored:
                    rel_proj_path = os.path.normpath(
                        os.path.relpath(package_for_project, sourcefolder)
                    )
                    relpaths_for_packagepaths[package_for_project] = rel_proj_path
    return relpaths_for_packagepaths


def find_java_source_files(directory, ignored_path_segments):
    java_file_paths = []
    for dirpath, _, files in os.walk(directory):
        java_file_paths.append(
            [os.path.join(dirpath, file) for file in files if file.endswith(".java")]
        )
    # ignored = any(ignored_segment in dirpath for ignored_segment in ignored_path_segments)
    return list(itertools.chain.from_iterable(java_file_paths))


def _find_sourcepackages_for_sourcefolder(sourcefolder):
    sourcepackage_paths = []
    for dirpath, _, files in os.walk(sourcefolder):
        java_filenames = [file for file in files if file.endswith(".java")]
        if java_filenames:
            sourcepackage_path = os.path.normpath(dirpath)
            sourcepackage_paths.append(sourcepackage_path)
    return sourcepackage_paths


def _find_sourcefolders_for_project(project_dir):
    classpath_file_path = os.path.join(project_dir, ".classpath")
    relative_sourcefolders = _parse_classpath(classpath_file_path)
    sourcefolders = [
        os.path.normpath(os.path.join(project_dir, folder))
        for folder in relative_sourcefolders
    ]
    return sourcefolders


def _parse_classpath(classpath_file_path):
    sourcefolders = []
    root = xml.etree.ElementTree.parse(classpath_file_path).getroot()
    for classpath in root.findall("classpathentry"):
        if classpath.get("kind") == "src":
            sourcefolders.append(classpath.get("path"))
    return sourcefolders
