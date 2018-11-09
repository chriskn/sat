import pyyed


class Graph:

    _GREEN = "#00DB43"
    _RED = "#FF0000"
    _MIN_NODE_SIZE = 50
    _MAX_NODE_SIZE = 200

    @staticmethod
    def cycle_graph(new_graph, old_graph, cycles):
        for cycle in cycles:
            for node_label in cycle:
                node_id = old_graph._id_for_name[node_label]
                node = old_graph.nodes()[node_id]
                new_graph.add_node(node.label, shape=node.shape,
                                   width=node.geom["width"], height=node.geom["height"], shape_fill=node.shape_fill)
            for edge in old_graph.edges().values():
                from_node = getattr(edge, "node1")
                to_node = getattr(edge, "node2")
                from_node_label = old_graph._name_for_id[int(from_node)]
                to_node_label = old_graph._name_for_id[int(to_node)]
                label = getattr(edge, "label")
                if from_node_label in cycle and to_node_label in cycle:
                    new_graph.add_edge(from_node_label, to_node_label, label)
        return new_graph

    def __init__(self):
        self._graph = pyyed.Graph()
        self._node_id = 0
        self._time = 0
        self._id_for_name = dict()
        self._name_for_id = dict()

    def add_node(self, label, package_group=None, shape="rectangle", width="50", height="50", shape_fill=_GREEN, node_type="ShapeNode", UML=False):
        if label not in self._id_for_name:
            if package_group:
                fqn = package_group.label+"."+label
                package_group.add_node(self._node_id,  label=label,
                                    shape=shape, width=width, height=height, shape_fill=shape_fill, node_type=node_type, UML=UML)
                self._id_for_name[fqn] = self._node_id
                self._name_for_id[self._node_id] = fqn
            else:    
                self._graph.add_node(self._node_id, label=label,
                                    shape=shape, width=width, height=height, shape_fill=shape_fill, node_type=node_type, UML=UML)
                self._id_for_name[label] = self._node_id
                self._name_for_id[self._node_id] = label
            self._node_id += 1
            return True
        return False

    def add_edge(self, source, target, label="", line_type="line", arrowhead="standard"):
        self._graph.add_edge(
            self._id_for_name[source], self._id_for_name[target], label=label, line_type=line_type, arrowhead=arrowhead)

    def add_group(self, label, shape="rectangle", fill="#ffd35b"):
        return self._graph.add_group(label, label=label, shape=shape, fill=fill)

    def cycles(self):
        cycles = self._do_trajan()
        named_cycles = []
        for cycle in cycles:
            named_cycles.append([self._name_for_id[_id] for _id in cycle])
        return named_cycles

    def _do_trajan(self):
        num_nodes = len(self._graph.nodes)
        dfs_pos = [-1] * (num_nodes)
        min_ancestor = [-1] * (num_nodes)
        stack_member = [False] * (num_nodes)
        strongly_connected_nodes = []
        for node in range(0, num_nodes):
            visited = dfs_pos[node] != -1
            if not visited:
                scn = self._scns(node, min_ancestor, dfs_pos,
                                 stack_member, [], strongly_connected_nodes)
                strongly_connected_nodes.append(scn)
        cycles = [cycle for cycle in strongly_connected_nodes if None !=
                  cycle and len(cycle) > 1]
        return cycles

    def _scns(self, node, min_ancestor, dfs_pos, on_stack, stack, cycles):
        dfs_pos[node] = self._time
        min_ancestor[node] = self._time
        self._time += 1
        stack.append(node)
        on_stack[node] = True
        adjacents = list(
            [edge.node2 for edge in self._graph.edges.values() if edge.node1 == node])
        for adjacent in adjacents:
            self._find_scns_in_adjacents(
                dfs_pos, adjacent, on_stack, min_ancestor, stack, cycles, node)
        is_head = min_ancestor[node] == dfs_pos[node]
        if is_head:
            scn = self._get_scn_from_stack(node, stack, on_stack)
            cycles.append(scn)

    def _find_scns_in_adjacents(self, dfs_pos, adjacent, on_stack, min_ancestor, stack, cycles, node):
        is_dfs_child = dfs_pos[adjacent] == -1
        visited = on_stack[adjacent] == True
        if is_dfs_child:
            self._scns(
                adjacent, min_ancestor, dfs_pos, on_stack, stack, cycles)
            min_ancestor[node] = min(
                min_ancestor[node], min_ancestor[adjacent])
        elif visited:
            min_ancestor[node] = min(min_ancestor[node], dfs_pos[adjacent])

    def _get_scn_from_stack(self, node, stack, on_stack):
        w = -1
        cycle = []
        while w != node:
            w = stack.pop()
            cycle.append(w)
            on_stack[w] = False
        return cycle

    def mark_cycles(self, cycles):
        for cycle in cycles:
            for nodeLabel in cycle:
                node = self._graph.nodes[self._id_for_name[nodeLabel]]
                setattr(node, "shape_fill", self._RED)
                for edge in self._graph.edges.values():
                    fromNode = self._name_for_id[getattr(edge, "node1")]
                    toNode = self._name_for_id[getattr(edge, "node2")]
                    if fromNode in cycle and toNode in cycle:
                        setattr(edge, "color", self._RED)

    def nodes(self): return self._graph.nodes

    def edges(self): return self._graph.edges

    def serialize(self): return self._graph.get_graph()

    def contains_node(self, label): return label in self._id_for_name

    def interpolate_node_size(self, numDependencies, maxNumDependencies):
        divisor = maxNumDependencies if maxNumDependencies > 0 else 1
        result = (numDependencies / divisor) * (self._MAX_NODE_SIZE -
                                                self._MIN_NODE_SIZE) + self._MIN_NODE_SIZE
        return str(round(result, 0))
