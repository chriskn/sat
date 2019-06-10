#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from sat.comp.domain import Project

_LOGGER = logging.getLogger("ProjectParser")


def parse_projects(project_dirs, packages):
    _LOGGER.info("Parsing Projects.")
    new_projects = []
    for proj_path, rel_proj_path in project_dirs.items():
        project = _parse_project(rel_proj_path, packages, proj_path)
        new_projects.append(project)
    return new_projects


def _parse_project(rel_proj_path, packages, proj_path):
    proj_name = rel_proj_path.replace(os.sep, ".")
    packages_for_proj = []
    for package in packages:
        is_package_in_project = proj_path in package.path
        if is_package_in_project:
            packages_for_proj.append(package)
    project = Project(proj_path, proj_name, packages_for_proj)
    return project
