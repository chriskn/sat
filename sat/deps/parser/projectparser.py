#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree

import sat.deps.parser.packageparser as parser
from sat.deps.domain import Project


def parse(directory, ignored_path_segments):
    projetc_paths = _scan(directory, ignored_path_segments)
    projects = [_parse_project(project_path) for project_path in projetc_paths]
    return projects


def _scan(directory, ignored_path_segments):
    projects = []
    for dirpath, _, files in os.walk(directory):
        ignored = any(
            ignored_segment in dirpath for ignored_segment in ignored_path_segments
        )
        if not ignored:
            for file in files:
                if file == ".classpath":
                    projects.append(dirpath)
    return projects


def _parse_project(project_path):
    classpath_file_path = os.path.join(project_path, ".classpath")
    relative_sourcefolders = _parse_classpath(classpath_file_path)
    sourcefolders = [os.path.join(project_path, s) for s in relative_sourcefolders]
    java_source_packages = parser.parse_packages(sourcefolders)
    project = Project(
        os.path.basename(project_path), project_path, java_source_packages
    )
    return project


def _parse_classpath(classpath_file_path):
    sourcefolders = []
    root = xml.etree.ElementTree.parse(classpath_file_path).getroot()
    for classpath in root.findall("classpathentry"):
        if classpath.get("kind") == "src":
            sourcefolders.append(classpath.get("path"))
    return sourcefolders
