"""Tests for the documented shortest-path contract and heap helpers."""

import pytest

from node import Node
from solution import get, insert_or_update, shortest_path_length


def make_graph(edges, *isolated_nodes):
    """Give every node its own adjacency lists, including isolated nodes."""
    names = set(isolated_nodes)
    for source, target, _ in edges:
        names.update((source, target))
    nodes = {
        name: Node(value=name, successors=[], predecessors=[],
                   incoming_nodes=[], outgoing_nodes=[])
        for name in names
    }
    lengths = {}
    for source, target, weight in edges:
        nodes[source].successors.append(nodes[target])
        lengths[nodes[source], nodes[target]] = weight
    return nodes, lengths


@pytest.mark.parametrize(
    "edges, expected",
    [
        pytest.param([("start", "goal", 7)], 7, id="single-edge"),
        pytest.param([("start", "goal", 0.25)], 0.25, id="fractional-weight"),
    ],
)
def test_shortest_path_length(edges, expected):
    nodes, lengths = make_graph(edges)
    assert shortest_path_length(lengths, nodes["start"], nodes["goal"]) == expected


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Dijkstra relaxation uses the successor's queued distance instead of "
           "the current path distance, losing accumulated costs and preventing improvements.",
)
@pytest.mark.parametrize(
    "edges, expected",
    [
        pytest.param([("start", "middle", 2), ("middle", "goal", 3)],
                     5, id="accumulate-path-length"),
        pytest.param([("start", "goal", 10), ("start", "middle", 2),
                      ("middle", "goal", 3)], 5, id="indirect-route-is-shorter"),
        pytest.param([("start", "a", 8), ("start", "b", 1),
                      ("b", "goal", 20), ("a", "goal", 1)],
                     9, id="choose-route-by-total-cost"),
        pytest.param([("start", "middle", 4), ("middle", "start", 1),
                      ("middle", "goal", 6)], 10, id="positive-cycle"),
        pytest.param([("start", "a", 1), ("start", "b", 4),
                      ("a", "goal", 9), ("b", "goal", 1)],
                     5, id="improve-existing-candidate"),
    ],
)
def test_shortest_path_length_with_multiple_edges(edges, expected):
    nodes, lengths = make_graph(edges)
    assert shortest_path_length(lengths, nodes["start"], nodes["goal"]) == expected


@pytest.mark.parametrize("edges", [[], [("start", "other", 2)]],
                         ids=["empty-graph", "disconnected-goal"])
def test_unreachable_goal(edges):
    nodes, lengths = make_graph(edges, "start", "goal")
    assert shortest_path_length(lengths, nodes["start"], nodes["goal"]) == float("inf")


@pytest.mark.parametrize("edges", [[], [("start", "other", 2)]])
def test_start_is_goal(edges):
    nodes, lengths = make_graph(edges, "start")
    assert shortest_path_length(lengths, nodes["start"], nodes["start"]) == 0


def test_edges_are_directed():
    nodes, lengths = make_graph([("goal", "start", 2)])
    assert shortest_path_length(lengths, nodes["start"], nodes["goal"]) == float("inf")


@pytest.mark.xfail(
    strict=True,
    raises=TypeError,
    reason="Equal distances cause heap tuples to compare Node instances, "
           "although the documented input does not require orderable nodes.",
)
def test_equal_cost_candidates_do_not_require_orderable_nodes():
    nodes, lengths = make_graph([
        ("start", "a", 1), ("start", "b", 1),
        ("a", "goal", 2), ("b", "goal", 4),
    ])
    assert shortest_path_length(lengths, nodes["start"], nodes["goal"]) == 3


def test_get_finds_distance_without_mutating_heap():
    first, second = object(), object()
    heap = [(2, first), (5, second)]
    assert get(heap, second) == 5
    assert heap == [(2, first), (5, second)]


def test_get_returns_zero_for_missing_node():
    assert get([], object()) == 0
    assert get([(3, object())], object()) == 0


def test_insert_or_update_inserts_new_node():
    first, second = object(), object()
    heap = [(5, first)]
    assert insert_or_update(heap, (2, second)) is None
    assert heap == [(2, second), (5, first)]


def test_insert_or_update_replaces_existing_entry():
    node = object()
    heap = [(5, node)]
    assert insert_or_update(heap, (2, node)) is None
    assert heap == [(2, node)]
