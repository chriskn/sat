#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from deps.graph.graph import Graph


class ProjectGraph(Graph):

    _CLASS_IMPORT_PATTERN = re.compile(r".*\.[A-Z].*")

    def __init__(self, projects):
        Graph.__init__(self)
        self._projects = projects
        numdeps = [len(p.imports()) for p in projects]
        max_numdeps = max(numdeps) if numdeps else 1
        for project in projects:
            self._add_node_for_project(project, max_numdeps)
            self._add_edges_for_project(project, projects, max_numdeps)

    def _add_edges_for_project(self, project, projects, max_numdeps):
        project_imports = self._collect_imports(project)
        for other_project in projects:
            for other_package in other_project.source_packages:
                is_imported_by_project = other_package.name in project_imports
                if is_imported_by_project:
                    other_not_yet_added = other_package.name not in self._id_for_name
                    if other_not_yet_added:
                        self._add_node_for_project(other_project, max_numdeps)
                    self.add_edge(project.name, other_project.name, "imports")

    def _add_node_for_project(self, project, max_numdeps):
        node_size = self.interpolate_node_size(len(project.imports()), max_numdeps)
        self.add_node(project.name, shape="ellipse", width=node_size, height=node_size)

    def _collect_imports(self, project):
        project_imports = []
        for imp in project.imports():
            if self._CLASS_IMPORT_PATTERN.match(imp):
                project_imports.append(re.split(r"\.[A-Z]", imp, maxsplit=1)[0])
            else:
                project_imports.append(imp)
        return project_imports

    def cycle_graph(self, cycles):
        graph = ProjectGraph([])
        Graph.create_cycle_graph(graph, self, cycles)
        return graph
