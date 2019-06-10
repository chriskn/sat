#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sat.scanner as scanner

import sat.comp.repo.packagerepo as package_repo
from sat.comp.parser import projectparser

_PROJECTS = dict()


def projects(workingdir, ignored_path_segments):
    key = workingdir + "".join(ignored_path_segments)
    analysed_projects = _PROJECTS.get(key)
    if analysed_projects:
        return analysed_projects
    project_dirs = scanner.find_projects(workingdir, ignored_path_segments)
    packages = package_repo.packages(workingdir, ignored_path_segments)
    analysed_projects = projectparser.parse_projects(project_dirs, packages)
    _PROJECTS[key] = analysed_projects
    return analysed_projects
