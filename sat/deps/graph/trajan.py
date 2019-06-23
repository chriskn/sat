#!/usr/bin/env python
# -*- coding: utf-8 -*-

# to many local vars and args
# pylint: disable=R0914,R0913


def do_trajan(graph, grouped=False):
    time = 0
    nodes = []
    if grouped:
        for group in graph.groups.values():
            nodes.extend(group.nodes.values())
    else:
        nodes = graph.nodes.values()
    num_nodes = len(nodes)
    dfs_pos = [-1] * (num_nodes)
    min_ancestor = [-1] * (num_nodes)
    stack_member = [False] * (num_nodes)
    strongly_connected_nodes = []
    for node in range(0, num_nodes):
        visited = dfs_pos[node] != -1
        if not visited:
            _scns(
                node,
                graph,
                min_ancestor,
                dfs_pos,
                stack_member,
                [],
                strongly_connected_nodes,
                grouped,
                nodes,
                time,
            )
    cycles = [cycle for cycle in strongly_connected_nodes if cycle and len(cycle) > 1]
    if grouped:
        g_cycles = []
        for cycle in cycles:
            g_cycle = [nodes[n].node_name for n in cycle]
            g_cycles.append(g_cycle)
        return g_cycles
    return cycles


def _scns(
    node, graph, min_ancestor, dfs_pos, on_stack, stack, cycles, grouped, nodes, time
):
    dfs_pos[node] = time
    min_ancestor[node] = time
    time += 1
    stack.append(node)
    on_stack[node] = True
    adjacents = []
    node_names = []
    for adj_node in nodes:
        node_names.append(adj_node.node_name)
    if grouped:
        for edge in graph.edges.values():
            source_node_name = edge.node1
            source_node_index = node_names.index(source_node_name)
            if source_node_index == node:
                target_node_id = edge.node2
                target_id = node_names.index(target_node_id)
                adjacents.append(target_id)
    else:
        adjacents = list(
            [edge.node2 for edge in graph.edges.values() if edge.node1 == node]
        )
    for adjacent in adjacents:
        _find_scns_in_adjacents(
            graph,
            dfs_pos,
            adjacent,
            on_stack,
            min_ancestor,
            stack,
            cycles,
            node,
            grouped,
            nodes,
            time,
        )
    is_head = min_ancestor[node] == dfs_pos[node]
    if is_head:
        scn = _scn_from_stack(node, stack, on_stack)
        cycles.append(scn)


def _find_scns_in_adjacents(
    graph,
    dfs_pos,
    adjacent,
    on_stack,
    min_ancestor,
    stack,
    cycles,
    node,
    grouped,
    nodes,
    time,
):
    is_dfs_child = dfs_pos[adjacent] == -1
    visited = on_stack[adjacent]
    if is_dfs_child:
        _scns(
            adjacent,
            graph,
            min_ancestor,
            dfs_pos,
            on_stack,
            stack,
            cycles,
            grouped,
            nodes,
            time,
        )
        min_ancestor[node] = min(min_ancestor[node], min_ancestor[adjacent])
    elif visited:
        min_ancestor[node] = min(min_ancestor[node], dfs_pos[adjacent])


def _scn_from_stack(node, stack, on_stack):
    node_from_stack = -1
    cycle = []
    while node_from_stack != node:
        node_from_stack = stack.pop()
        cycle.append(node_from_stack)
        on_stack[node_from_stack] = False
    return cycle
