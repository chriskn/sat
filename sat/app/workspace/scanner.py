import os
import itertools
import sat.app.workspace.parser.classpath_parser as cpparser


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


def find_bundles(directory, ignored_path_segments):
    bundel_paths = set()
    for dirpath, _, files in os.walk(directory):
        ignored = any(
            ignored_segment in dirpath for ignored_segment in ignored_path_segments
        )
        if not ignored:
            for file in files:
                if file == "MANIFEST.MF":
                    bundel_paths.add(os.path.dirname(dirpath))
    return bundel_paths


def find_packages(directory, ignored_path_segments):
    project_dirs = find_projects(directory, ignored_path_segments)
    relpaths_for_packagepaths = dict()
    for project_dir in project_dirs:
        sourcefolders_for_project = find_sourcefolders_for_project(project_dir)
        for sourcefolder in sourcefolders_for_project:
            packages_for_sourcefolder = find_packages_for_sourcefolder(
                sourcefolder, ignored_path_segments
            )
            for package_for_project in packages_for_sourcefolder:
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


def find_sourcefiles(directory, ignored_path_segments):
    java_file_paths = []
    for dirpath, _, files in os.walk(directory):
        ignored = any(
            ignored_segment in dirpath for ignored_segment in ignored_path_segments
        )
        if not ignored:
            java_file_paths.append(
                [
                    os.path.join(dirpath, file_)
                    for file_ in files
                    if file_.endswith(".java")
                ]
            )
    return list(itertools.chain.from_iterable(java_file_paths))


def find_packages_for_sourcefolder(sourcefolder, ignored_path_segments):
    package_paths = []
    for dirpath, _, files in os.walk(sourcefolder):
        ignored = any(
            ignored_segment in dirpath for ignored_segment in ignored_path_segments
        )
        if not ignored:
            java_filenames = [file for file in files if file.endswith(".java")]
            if java_filenames:
                package_path = os.path.abspath(dirpath)
                package_paths.append(package_path)
    return package_paths


def find_sourcefolders_for_project(project_dir):
    classpath_file_path = os.path.join(project_dir, ".classpath")
    relative_sourcefolders = cpparser.parse_classpath(classpath_file_path)
    sourcefolders = [
        os.path.normpath(os.path.join(project_dir, folder))
        for folder in relative_sourcefolders
    ]
    return sourcefolders
