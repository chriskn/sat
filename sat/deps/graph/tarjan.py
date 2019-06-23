#!/usr/bin/env python
# -*- coding: utf-8 -*-

# to many local vars and args
# pylint: disable=R0914,R0913


def scns(graph, grouped=False):
    repetition = 0
    nodes = []
    if grouped:
        for group in graph.groups.values():
            nodes.extend(group.nodes.values())
    else:
        nodes = graph.nodes.values()
    num_nodes = len(nodes)
    edges = graph.edges.values()
    df_search_pos = [-1] * (num_nodes)
    min_ancestor = [-1] * (num_nodes)
    stack_member = [False] * (num_nodes)
    stack = []
    strongly_connected_nodes = []
    for node_id in range(0, num_nodes):
        visited = df_search_pos[node_id] != -1
        if not visited:
            _find_scns(
                node_id,
                nodes,
                edges,
                min_ancestor,
                df_search_pos,
                stack_member,
                stack,
                strongly_connected_nodes,
                grouped,
                repetition,
            )
    cycles = [cycle for cycle in strongly_connected_nodes if cycle and len(cycle) > 1]
    if grouped:
        g_cycles = []
        for cycle in cycles:
            g_cycle = [nodes[n].node_name for n in cycle]
            g_cycles.append(g_cycle)
        return g_cycles
    return cycles


def _find_scns(
    node_id,
    nodes,
    edges,
    min_ancestor,
    df_search_pos,
    on_stack,
    stack,
    strongly_connected_nodes,
    grouped,
    repetition,
):
    df_search_pos[node_id] = repetition
    min_ancestor[node_id] = repetition
    repetition += 1
    stack.append(node_id)
    on_stack[node_id] = True
    adjacents = []
    node_names = [node.node_name for node in nodes]
    if grouped:
        for edge in edges:
            source_node_name = edge.node1
            source_node_index = node_names.index(source_node_name)
            if source_node_index == node_id:
                target_node_id = edge.node2
                target_id = node_names.index(target_node_id)
                adjacents.append(target_id)
    else:
        adjacents = list([edge.node2 for edge in edges if edge.node1 == node_id])
    for adjacent in adjacents:
        _find_scns_in_adjacents(
            node_id,
            nodes,
            edges,
            df_search_pos,
            adjacent,
            on_stack,
            min_ancestor,
            stack,
            strongly_connected_nodes,
            grouped,
            repetition,
        )
    is_head = min_ancestor[node_id] == df_search_pos[node_id]
    if is_head:
        scn_cycle = _cycle_from_stack(node_id, stack, on_stack)
        strongly_connected_nodes.append(scn_cycle)


def _find_scns_in_adjacents(
    node_id,
    nodes,
    edges,
    df_search_pos,
    adjacent,
    on_stack,
    min_ancestor,
    stack,
    strongly_connected_nodes,
    grouped,
    repetition,
):
    was_not_part_in_dfs = df_search_pos[adjacent] == -1
    visited = on_stack[adjacent]
    if was_not_part_in_dfs:
        _find_scns(
            adjacent,
            nodes,
            edges,
            min_ancestor,
            df_search_pos,
            on_stack,
            stack,
            strongly_connected_nodes,
            grouped,
            repetition,
        )
        min_ancestor[node_id] = min(min_ancestor[node_id], min_ancestor[adjacent])
    elif visited:
        min_ancestor[node_id] = min(min_ancestor[node_id], df_search_pos[adjacent])


def _cycle_from_stack(node, stack, on_stack):
    node_from_stack = -1
    cycle = []
    while node_from_stack != node:
        node_from_stack = stack.pop()
        cycle.append(node_from_stack)
        on_stack[node_from_stack] = False
    return cycle
