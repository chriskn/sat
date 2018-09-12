import pyyed

class Graph: 

    _pyyedGraph = pyyed.Graph() 
    _nodeId = 0
    _time = 0
    _idForNames = dict()
    _namesForId = dict()
    _GREEN = "#00DB43"
    _RED = "#FF0000"

    def addNode(self, label , shape="ellipse", width="50", height="50", color=_GREEN):
        if label not in self._idForNames:
            self._idForNames[label] = str(self._nodeId)
            self._namesForId[self._nodeId] = label
            self._pyyedGraph.add_node(str(self._nodeId), label=label, shape=shape, width=width, height=height, shape_fill=color)
            self._nodeId += 1
            return True
        return False
    
    def addEdge(self, source, target, label):
        self._pyyedGraph.add_edge(self._idForNames[source], self._idForNames[target], label=label)

    def _findCyclesRecursive(self, node, low, disc, stackMember, stack, cycles):
        disc[node] = self._time
        low[node] = self._time
        self._time += 1
        stackMember[node] = True
        stack.append(node)
        adjacentNodes = list([int(edge.node2) for edge in self._pyyedGraph.edges.values() if int(edge.node1) == node])
        for adjacent in adjacentNodes:
            if disc[adjacent] == -1 :
                self._findCyclesRecursive(adjacent, low, disc, stackMember, stack, cycles)
                low[node] = min(low[node], low[adjacent])
            elif stackMember[adjacent] == True: 
                low[node] = min(low[node], disc[adjacent])
        # head node found, pop the stack and add SSC
        w = -1
        if low[node] == disc[node]:
            cycle = []
            while w != node:
                w = stack.pop()
                cycle.append(w)
                stackMember[w] = False
            cycles.append(cycle)

    #The function to do DFS traversal. 
    def getCycles(self):
        numNodes = len(self._pyyedGraph.nodes)
        disc = [-1] * (numNodes)
        low = [-1] * (numNodes)
        stackMember = [False] * (numNodes)
        st =[]
        cycles = []
        for node in range(0,numNodes):
            if disc[node] == -1:
                cycles.append(self._findCyclesRecursive(node, low, disc, stackMember, st, cycles))
        return [cycle for cycle in cycles if None != cycle and len(cycle) > 1]
    
    def markCycles(self, cycles):
        for cycle in cycles:
            for nodeId in cycle:
                node = self._pyyedGraph.nodes[str(nodeId)]
                setattr(node, "shape_fill", self._RED)
                for edge in self._pyyedGraph.edges.values():
                    fromNode = int(getattr(edge, "node1"))
                    toNode = int(getattr(edge, "node2"))
                    if fromNode in cycle and toNode in cycle:
                        setattr(edge, "color", self._RED)


    def getNodes(self): return self._pyyedGraph.nodes

    def getEdges(self): return self._pyyedGraph.edges

    def serialize(self): return self._pyyedGraph.get_graph()