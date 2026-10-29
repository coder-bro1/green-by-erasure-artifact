"""Tests for topological ordering, including documented existing limitations."""

import pytest

from node import Node
from solution import topological_ordering


def make_graph(values, edges):
    """Build a graph without relying on Node's shared mutable defaults."""
    nodes = {
        value: Node(value=value, incoming_nodes=[], outgoing_nodes=[])
        for value in values
    }
    for source, target in edges:
        nodes[source].outgoing_nodes.append(nodes[target])
        nodes[target].incoming_nodes.append(nodes[source])
    return nodes


def assert_topological_order(result, nodes):
    """Check completeness, uniqueness, and every edge's relative order."""
    assert len(result) == len(nodes)
    assert set(result) == set(nodes)
    positions = {node: index for index, node in enumerate(result)}
    for node in nodes:
        for target in node.outgoing_nodes:
            assert positions[node] < positions[target]


@pytest.mark.parametrize(
    ("values", "edges", "input_order"),
    [
        ([], [], []),
        (["a"], [], ["a"]),
        (["a", "b", "c"], [], ["c", "a", "b"]),
        (["a", "b"], [("a", "b")], ["b", "a"]),
        (["a", "b", "c"], [("a", "b"), ("a", "c")], ["c", "b", "a"]),
        (["a", "b", "c"], [("a", "c"), ("b", "c")], ["c", "b", "a"]),
        (
            ["a", "b", "c", "d", "e"],
            [("a", "b"), ("c", "d")],
            ["d", "b", "e", "c", "a"],
        ),
    ],
    ids=["empty", "singleton", "isolated", "edge", "fan-out", "fan-in", "disconnected"],
)
def test_topological_order_for_supported_graphs(values, edges, input_order):
    graph = make_graph(values, edges)
    nodes = [graph[value] for value in input_order]

    assert_topological_order(topological_ordering(nodes), nodes)


def test_isolated_nodes_keep_input_order():
    graph = make_graph(["a", "b", "c"], [])
    nodes = [graph["c"], graph["a"], graph["b"]]

    result = topological_ordering(nodes)

    assert result == nodes
    assert result is not nodes


def test_shared_sink_is_included_only_once():
    graph = make_graph(["a", "b", "sink"], [("a", "sink"), ("b", "sink")])

    result = topological_ordering(list(graph.values()))

    assert result == [graph["a"], graph["b"], graph["sink"]]


def test_input_and_adjacency_lists_are_not_modified():
    graph = make_graph(["a", "b", "c"], [("a", "b"), ("a", "c")])
    nodes = list(reversed(graph.values()))
    original_nodes = nodes.copy()
    original_adjacency = {
        node: (node.incoming_nodes.copy(), node.outgoing_nodes.copy())
        for node in nodes
    }

    first_result = topological_ordering(nodes)
    second_result = topological_ordering(nodes)

    assert first_result == second_result
    assert nodes == original_nodes
    for node, (incoming, outgoing) in original_adjacency.items():
        assert node.incoming_nodes == incoming
        assert node.outgoing_nodes == outgoing


@pytest.mark.xfail(
    strict=True,
    reason="Existing bug: eligibility checks outgoing edges instead of incoming prerequisites.",
)
@pytest.mark.parametrize(
    ("values", "edges"),
    [
        (["a", "b", "c"], [("a", "b"), ("b", "c")]),
        (
            ["a", "b", "c", "d"],
            [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")],
        ),
    ],
    ids=["chain", "diamond"],
)
def test_multilevel_graph_contains_every_node_in_topological_order(values, edges):
    graph = make_graph(values, edges)
    nodes = list(graph.values())

    assert_topological_order(topological_ordering(nodes), nodes)
