from graph import Graph

class ProjectGraph(Graph):

    def __init__(self, projects=[]):
        Graph.__init__(self)
        self._projects = projects
        numdeps = [len(p.imports()) for p in projects]
        max_numdeps = max(numdeps) if len (numdeps)> 0  else 1 
        for project in projects:
            node_size = self.interpolate_node_size(len(project.imports()), max_numdeps)
            self.add_node(project.name, width=node_size, height=node_size)
            project_imports = project.imports()
            for other_project in projects:
                for other_package in other_project.source_packages:
                    if other_package.name in project_imports:
                        if other_package.name not in self._id_for_name:
                            node_size = self.interpolate_node_size(len(other_project.imports()), max_numdeps)
                            self.add_node(other_project.name, width=node_size, height=node_size)                           
                        self.add_edge(project.name, other_project.name, "imports")

    def cycle_graph(self, cycles):
        graph = ProjectGraph()
        for cycle in cycles:
            for node_label in cycle:
                node_id = self._id_for_name[node_label]
                node = self._graph.nodes[node_id]
                graph.add_node(node.label, shape=node.shape, width=node.geom["width"], height=node.geom["height"], color=node.shape_fill) 
            for edge in self._graph.edges.values():
                from_node = getattr(edge, "node1")
                to_node = getattr(edge, "node2")
                from_node_label = self._name_for_id[int(from_node)]
                to_node_label = self._name_for_id[int(to_node)]
                label =  getattr(edge, "label")
                if from_node_label in cycle and to_node_label in cycle:
                    graph.add_edge(from_node_label, to_node_label, label)
        return graph
