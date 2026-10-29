"""Tests for the acyclic-graph contract of topological_ordering."""

from collections.abc import Set
from itertools import combinations, permutations

import pytest

from node import Node
from solution import topological_ordering


def make_graph(size, edges):
    # Supply fresh adjacency lists to avoid Node's shared default arguments.
    nodes = [Node(value=i, incoming_nodes=[], outgoing_nodes=[]) for i in range(size)]
    for source, destination in edges:
        nodes[source].outgoing_nodes.append(nodes[destination])
        nodes[destination].incoming_nodes.append(nodes[source])
    return nodes


def assert_topological_order(result, nodes):
    ordered = list(result)
    assert len(ordered) == len(nodes)
    assert set(ordered) == set(nodes)
    positions = {node: index for index, node in enumerate(ordered)}
    for node in nodes:
        for successor in node.outgoing_nodes:
            assert positions[node] < positions[successor]


@pytest.mark.parametrize(
    "size, edges",
    [
        (0, []),
        (1, []),
        (4, []),
        (4, [(0, 1), (1, 2), (2, 3)]),
        (4, [(0, 1), (0, 2), (0, 3)]),
        (4, [(0, 3), (1, 3), (2, 3)]),
        (4, [(0, 1), (0, 2), (1, 3), (2, 3)]),
        (6, [(0, 1), (1, 2), (3, 4)]),
        (5, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (0, 4)]),
    ],
    ids=[
        "empty", "singleton", "isolated", "chain", "fan-out", "fan-in",
        "diamond", "disconnected", "transitive-edges",
    ],
)
def test_orders_all_nodes_before_their_successors(size, edges):
    nodes = make_graph(size, edges)
    # Reverse the input so a chain cannot pass by simply returning the input.
    assert_topological_order(topological_ordering(nodes[::-1]), nodes)


def test_all_four_node_dags_with_every_input_order():
    # Every four-node DAG has a vertex labeling with edges going forward.
    possible_edges = list(combinations(range(4), 2))
    for mask in range(1 << len(possible_edges)):
        edges = [edge for bit, edge in enumerate(possible_edges) if mask & (1 << bit)]
        nodes = make_graph(4, edges)
        for input_order in permutations(nodes):
            assert_topological_order(topological_ordering(list(input_order)), nodes)


def test_does_not_mutate_input_or_adjacency_lists_and_is_repeatable():
    nodes = make_graph(4, [(0, 1), (0, 2), (1, 3), (2, 3)])
    nodes.reverse()
    original_nodes = nodes.copy()
    adjacency = [(node.incoming_nodes.copy(), node.outgoing_nodes.copy()) for node in nodes]

    first = topological_ordering(nodes)
    second = topological_ordering(nodes)

    assert_topological_order(first, nodes)
    assert list(first) == list(second)
    assert nodes == original_nodes
    for node, (incoming, outgoing) in zip(nodes, adjacency):
        assert node.incoming_nodes == incoming
        assert node.outgoing_nodes == outgoing


@pytest.mark.xfail(
    strict=True,
    reason="The docstring promises an OrderedSet, but topological_ordering returns a list.",
)
def test_returns_an_ordered_set():
    nodes = make_graph(2, [(0, 1)])
    result = topological_ordering(nodes)
    assert isinstance(result, Set), "The docstring promises an OrderedSet return value"
    assert list(result) == nodes
