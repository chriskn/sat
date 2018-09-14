from repr import Graph
from project.project import Package
from copy import deepcopy
import pyyed

class PackageGraph(Graph):

    _packages = None

    def __init__(self, packages=[]):
        Graph.__init__(self)
        self._packages = packages
        for package in packages:
            self.addNode(package.name)
            for imp in package.getImports():
                if not self.containsNode(imp):
                    self.addNode(imp)
                self.addEdge(package.name, imp, "imports")
    
    def getCycleGraph(self, cycles):
        graph = PackageGraph()
        cycleNodes = []
        for cycle in cycles:
            for nodeLabel in cycle:
                nodeId = self._idForNames[nodeLabel]
                node = self._graph.nodes[nodeId]
                cycleNodes.append(node)
                nodeIdsInGraph = [node.node_name for node in graph._graph.nodes.values()]
                if  nodeId not in nodeIdsInGraph:
                    graph.addNode(node.node_name, shape=node.shape, width=node.geom["width"], height=node.geom["height"], color=node.shape_fill) 
        for edge in self._graph.edges.values():
            fromNode = self._namesForId[int(getattr(edge, "node1"))]
            toNode = self._namesForId[int(getattr(edge, "node2"))]
            label =  getattr(edge, "label")
            if fromNode in cycle and toNode in cycle:
                graph.addEdge(fromNode, toNode, label)
        return graph
