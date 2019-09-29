#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import re

_CLASS_IMPORT_PATTERN = re.compile(r".*\.[A-Z].*")


def project_coupling_dataframe(projects):
    proj_names = []
    data = []
    for project in reversed(projects):
        proj_names.append(project.name)
        proj_imports = [_to_package_import(imp) for imp in project.imports()]
        proj_data = _calculate_project_coupling(projects, proj_imports)
        data.append(proj_data)
    return pd.DataFrame(data=data, index=proj_names, columns=list(reversed(proj_names)))


def _calculate_project_coupling(projects, proj_imports):
    proj_data = []
    for other_project in projects:
        other_project_packages = {package.name for package in other_project.packages}
        proj_deps = sum(
            [
                proj_imports.count(other_package_package)
                for other_package_package in other_project_packages
            ]
        )
        proj_data.append(proj_deps)
    return proj_data


def package_coupling_dataframe(packages):
    names = [p.name for p in packages]
    data = []
    for package in reversed(packages):
        package_imps = [_to_package_import(imp) for imp in package.imports()]
        data.append([package_imps.count(pName) for pName in names])
    data_frame = pd.DataFrame(data=data, index=list(reversed(names)), columns=names)
    return data_frame


def num_packages_importing_package(all_packages, package_to_analyse):
    num_packages_importing_package = 0
    for package in all_packages:
        package_imports_for_package = {
            _to_package_import(imp) for imp in package.imports()
        }
        if package_to_analyse.name in package_imports_for_package:
            num_packages_importing_package += 1
    return num_packages_importing_package


def num_packages_imported_by_package(package_to_analyse):
    return len(
        {
            _to_package_import(imp)
            for imp in package_to_analyse.imports()
            if _to_package_import(imp) is not package_to_analyse.name
        }
    )


def _to_package_import(import_):
    if _CLASS_IMPORT_PATTERN.match(import_):
        return re.split(r"\.[A-Z]", import_, maxsplit=1)[0]
    return import_
