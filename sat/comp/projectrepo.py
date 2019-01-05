#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

import comp.compcalculator as comp
import comp.packagerepo as prepo
import scanner
from comp.domain import Project

_projects = dict()
_logger = logging.getLogger("ProjectRepo")


def projects(workingdir, ignored_path_segments):
    key = workingdir+"".join(ignored_path_segments)
    projects = _projects.get(key)
    if projects:
        return projects
    project_dirs = scanner.find_projects(
        workingdir, ignored_path_segments)
    packages = prepo.packages(workingdir, ignored_path_segments)
    projects = _parse_projects(project_dirs, packages)
    _projects[key] = projects
    return projects


def _parse_projects(project_dirs, packages):
    _logger.info("Parsing Projects.")
    projects = []
    for proj_path, rel_proj_path in project_dirs.items():
        proj_name = rel_proj_path.replace(os.sep, ".")
        packages_for_proj = []
        for package in packages:
            if _is_under_project(package.path, proj_path):
                packages_for_proj.append(package)
        project = Project(proj_path, proj_name, packages_for_proj)
        projects.append(project)
    return projects


def _is_under_project(package_path, proj_path):
    if proj_path in package_path:
        return True
    return False
