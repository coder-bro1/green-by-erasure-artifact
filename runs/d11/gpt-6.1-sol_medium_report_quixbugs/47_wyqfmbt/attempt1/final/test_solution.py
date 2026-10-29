"""Tests for the documented minimum-weight paths contract."""

import math

import pytest

from solution import shortest_paths


@pytest.mark.parametrize("source", ["A", 0, -1, None, ("node", 1)])
def test_empty_graph_has_zero_distance_to_source(source):
    assert shortest_paths(source, {}) == {source: 0}


@pytest.mark.parametrize("weight", [0, 1, 2.5])
def test_nonnegative_source_self_loop(weight):
    assert shortest_paths("A", {("A", "A"): weight}) == {"A": 0}


def test_disconnected_cycle_is_unreachable():
    graph = {("B", "C"): -2, ("C", "B"): 3}
    assert shortest_paths("A", graph) == {
        "A": 0,
        "B": math.inf,
        "C": math.inf,
    }


@pytest.mark.xfail(
    strict=True,
    reason="Relaxation updates weight_by_edge instead of weight_by_node, leaving reachable distances infinite.",
)
@pytest.mark.parametrize(
    "source, graph, expected",
    [
        pytest.param(
            "A",
            {
                ("A", "B"): 3,
                ("A", "C"): 3,
                ("A", "F"): 5,
                ("C", "B"): -2,
                ("C", "D"): 7,
                ("C", "E"): 4,
                ("D", "E"): -5,
                ("E", "F"): -1,
            },
            {"A": 0, "C": 3, "B": 1, "E": 5, "D": 10, "F": 4},
            id="docstring-example",
        ),
        pytest.param("A", {("A", "B"): 7}, {"A": 0, "B": 7}, id="positive-edge"),
        pytest.param("A", {("A", "B"): 0}, {"A": 0, "B": 0}, id="zero-edge"),
        pytest.param("A", {("A", "B"): -4}, {"A": 0, "B": -4}, id="negative-edge"),
        pytest.param(
            "A",
            {("C", "D"): 4, ("B", "C"): 3, ("A", "B"): 2},
            {"A": 0, "B": 2, "C": 5, "D": 9},
            id="reverse-ordered-chain-needs-repeated-relaxation",
        ),
        pytest.param(
            "A",
            {("A", "C"): 10, ("A", "B"): 2, ("B", "C"): 3},
            {"A": 0, "B": 2, "C": 5},
            id="indirect-path-beats-direct-edge",
        ),
        pytest.param(
            "A",
            {("A", "B"): 2, ("B", "C"): -4, ("C", "A"): 3},
            {"A": 0, "B": 2, "C": -2},
            id="negative-edge-in-positive-weight-cycle",
        ),
        pytest.param(
            "A",
            {("A", "B"): 2, ("B", "A"): -2},
            {"A": 0, "B": 2},
            id="zero-weight-cycle",
        ),
        pytest.param(
            "A",
            {("A", "B"): 0.5, ("B", "C"): 0.25, ("A", "C"): 1.5},
            {"A": 0, "B": 0.5, "C": 0.75},
            id="fractional-weights",
        ),
        pytest.param(
            0,
            {(0, 1): 3, (1, 2): -1},
            {0: 0, 1: 3, 2: 2},
            id="integer-node-identifiers",
        ),
        pytest.param(
            "A",
            {("A", "B"): 2, ("C", "D"): 1, ("D", "C"): 1},
            {"A": 0, "B": 2, "C": math.inf, "D": math.inf},
            id="reachable-and-disconnected-components",
        ),
    ],
)
def test_minimum_path_weights(source, graph, expected):
    assert shortest_paths(source, graph.copy()) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Only edge destinations are initialized; an origin-only non-source node causes KeyError.",
)
@pytest.mark.parametrize(
    "graph, expected",
    [
        pytest.param(
            {("B", "A"): 2},
            {"A": 0, "B": math.inf},
            id="incoming-edge-does-not-make-origin-reachable",
        ),
        pytest.param(
            {("B", "C"): 2},
            {"A": 0, "B": math.inf, "C": math.inf},
            id="disconnected-origin-only-node",
        ),
    ],
)
def test_all_edge_endpoints_are_included(graph, expected):
    assert shortest_paths("A", graph.copy()) == expected
