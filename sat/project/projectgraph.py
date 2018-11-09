from graph import Graph

class ProjectGraph(Graph):

    def __init__(self, projects=[]):
        Graph.__init__(self)
        self._projects = projects
        numdeps = [len(p.imports()) for p in projects]
        max_numdeps = max(numdeps) if len (numdeps)> 0  else 1 
        for project in projects:
            node_size = self.interpolate_node_size(len(project.imports()), max_numdeps)
            self.add_node(project.name, shape="ellipse", width=node_size, height=node_size)
            project_imports = project.imports()
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
