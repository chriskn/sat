from graph import Graph

class ProjectGraph(Graph):

    def __init__(self, projects=[]):
        Graph.__init__(self)
        self._projects = projects
        numDeps = [len(p.getImports()) for p in projects]
        maxNumberDependencies = max(numDeps) if len (numDeps)> 0  else 1            
        for project in projects:
            nodeSize = self.interpolateLinear(len(project.getImports()), maxNumberDependencies)
            self.addNode(project.name, width=nodeSize, height=nodeSize)
            pImports = project.getImports()
            for oProject in projects:
                for oPackage in oProject.sourcePackages:
                    if oPackage.name in pImports:
                        if oPackage.name not in self._idForNames:
                            nodeSize = self.interpolateLinear(len(oProject.getImports()), maxNumberDependencies)
                            self.addNode(oProject.name, width=nodeSize, height=nodeSize)                           
                        self.addEdge(project.name, oProject.name, "imports")

    def getCycleGraph(self, cycles):
        graph = ProjectGraph()
        for cycle in cycles:
            for nodeLabel in cycle:
                nodeId = self._idForNames[nodeLabel]
                node = self._graph.nodes[nodeId]
                graph.addNode(node.label, shape=node.shape, width=node.geom["width"], height=node.geom["height"], color=node.shape_fill) 
            for edge in self._graph.edges.values():
                fromNode = getattr(edge, "node1")
                toNode = getattr(edge, "node2")
                fromNodeLabel = self._namesForId[int(fromNode)]
                toNodeLabel = self._namesForId[int(toNode)]
                label =  getattr(edge, "label")
                if fromNodeLabel in cycle and toNodeLabel in cycle:
                    graph.addEdge(fromNodeLabel, toNodeLabel, label)
        return graph
