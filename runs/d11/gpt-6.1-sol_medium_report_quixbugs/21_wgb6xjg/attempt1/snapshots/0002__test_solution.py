"""Tests for the documented acyclic-graph contract in solution.py."""

from collections.abc import Set

import pytest

from node import Node
from solution import topological_ordering


def make_graph(labels, edges):
    # Supply fresh adjacency lists to avoid Node's shared mutable defaults.
    nodes = {
        label: Node(value=label, incoming_nodes=[], outgoing_nodes=[])
        for label in labels
    }
    for source, target in edges:
        nodes[source].outgoing_nodes.append(nodes[target])
        nodes[target].incoming_nodes.append(nodes[source])
    return [nodes[label] for label in labels]


def assert_topological_order(nodes, result):
    ordered = list(result)
    assert len(ordered) == len(nodes), "Every input node must occur exactly once"
    assert set(ordered) == set(nodes), "The output must contain exactly the input nodes"
    positions = {node: index for index, node in enumerate(ordered)}
    for node in nodes:
        for target in node.outgoing_nodes:
            assert positions[node] < positions[target], "An edge must point forward"


@pytest.mark.parametrize(
    "labels, edges",
    [
        pytest.param([], [], id="empty"),
        pytest.param(["a"], [], id="single-node"),
        pytest.param(["c", "a", "b"], [], id="isolated-nodes"),
        pytest.param(["a", "b"], [("a", "b")], id="single-edge"),
        pytest.param(["b", "a"], [("a", "b")], id="reverse-input-order"),
        pytest.param(
            ["c", "b", "a"], [("a", "b"), ("a", "c")], id="fork"
        ),
        pytest.param(
            ["c", "b", "a"], [("a", "c"), ("b", "c")], id="join"
        ),
        pytest.param(
            ["d", "b", "isolated", "c", "a"],
            [("a", "b"), ("c", "d")],
            id="disconnected-components",
        ),
        pytest.param(
            ["c", "b", "a"],
            [("a", "b"), ("b", "c")],
            id="three-node-chain",
            marks=pytest.mark.xfail(
                strict=True,
                reason="Checks outgoing neighbors instead of completed predecessors; omits b and c",
            ),
        ),
        pytest.param(
            ["d", "c", "b", "a"],
            [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")],
            id="diamond",
            marks=pytest.mark.xfail(
                strict=True,
                reason="Checks outgoing neighbors instead of predecessors; omits both middle nodes and sink",
            ),
        ),
        pytest.param(
            ["a", "b", "c"],
            [("a", "b"), ("a", "c"), ("b", "c")],
            id="chain-with-shortcut",
            marks=pytest.mark.xfail(
                strict=True,
                reason="Appends sink c before considering b again, so the result omits b",
            ),
        ),
    ],
)
def test_contains_all_nodes_in_topological_order(labels, edges):
    nodes = make_graph(labels, edges)
    assert_topological_order(nodes, topological_ordering(nodes))


def test_does_not_modify_input_graph():
    nodes = make_graph(["b", "a", "c"], [("a", "b"), ("a", "c")])
    original_nodes = list(nodes)
    original_edges = {
        node: (list(node.incoming_nodes), list(node.outgoing_nodes)) for node in nodes
    }

    result = topological_ordering(nodes)

    assert_topological_order(nodes, result)
    assert nodes == original_nodes
    for node, (incoming, outgoing) in original_edges.items():
        assert node.incoming_nodes == incoming
        assert node.outgoing_nodes == outgoing


@pytest.mark.xfail(
    strict=True,
    reason="The docstring promises an OrderedSet, but the function returns a plain list",
)
def test_returns_an_ordered_set():
    nodes = make_graph(["b", "a"], [("a", "b")])
    result = topological_ordering(nodes)

    assert_topological_order(nodes, result)
    assert isinstance(result, Set), "An OrderedSet must implement the set interface"
