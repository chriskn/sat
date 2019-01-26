#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import scanner

import comp.repo.packagerepo as prepo
from comp.domain import Project

_PROJECTS = dict()
_LOGGER = logging.getLogger("ProjectRepo")


def projects(workingdir, ignored_path_segments):
    key = workingdir + "".join(ignored_path_segments)
    analysed_projects = _PROJECTS.get(key)
    if analysed_projects:
        return analysed_projects
    project_dirs = scanner.find_projects(
        workingdir, ignored_path_segments)
    packages = prepo.packages(workingdir, ignored_path_segments)
    analysed_projects = _parse_projects(project_dirs, packages)
    _PROJECTS[key] = analysed_projects
    return analysed_projects


def _parse_projects(project_dirs, packages):
    _LOGGER.info("Parsing Projects.")
    new_projects = []
    for proj_path, rel_proj_path in project_dirs.items():
        proj_name = rel_proj_path.replace(os.sep, ".")
        packages_for_proj = []
        for package in packages:
            if _is_under_project(package.path, proj_path):
                packages_for_proj.append(package)
        project = Project(proj_path, proj_name, packages_for_proj)
        new_projects.append(project)
    return new_projects


def _is_under_project(package_path, proj_path):
    if proj_path in package_path:
        return True
    return False
