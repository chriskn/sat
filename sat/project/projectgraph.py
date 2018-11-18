#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graph import Graph
import re

class ProjectGraph(Graph):

    _CLASS_IMPORT_PATTERN = re.compile(r'.*\.[A-Z].*')

    def __init__(self, projects=[]):
        Graph.__init__(self)
        self._projects = projects
        numdeps = [len(p.imports()) for p in projects]
        max_numdeps = max(numdeps) if len (numdeps)> 0  else 1 
        for project in projects:
            node_size = self.interpolate_node_size(len(project.imports()), max_numdeps)
            self.add_node(project.name, shape="ellipse", width=node_size, height=node_size)
            project_imports = []
            for imp in project.imports():
                if self._CLASS_IMPORT_PATTERN.match(imp):
                    project_imports.append(re.split(r'\.[A-Z]', imp, maxsplit=1)[0])
                else:
                    project_imports.append(imp)
            for other_project in projects:
                for other_package in other_project.source_packages:        
                    if other_package.name in project_imports:
                        if other_package.name not in self._id_for_name:
                            node_size = self.interpolate_node_size(len(other_project.imports()), max_numdeps)
                            self.add_node(other_project.name, shape="ellipse", width=node_size, height=node_size)                           
                        self.add_edge(project.name, other_project.name, "imports")

    def cycle_graph(self, cycles):
        graph = ProjectGraph()
        Graph.cycle_graph(graph, self , cycles)
        return graph
