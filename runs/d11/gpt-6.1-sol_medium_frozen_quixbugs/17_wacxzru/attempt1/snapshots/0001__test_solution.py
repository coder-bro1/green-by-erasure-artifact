"""Contract tests; strict xfails document known defects in solution.py."""

import math

import pytest

from solution import shortest_paths


@pytest.mark.parametrize("source", ["A", 0, ("node", 1)])
def test_empty_graph_contains_source_with_zero_distance(source):
    assert shortest_paths(source, {}) == {source: 0}


@pytest.mark.parametrize("weight", [0, 1, 2.5])
def test_nonnegative_source_self_loop(weight):
    assert shortest_paths("A", {("A", "A"): weight}) == {"A": 0}


def test_unreachable_cycle_has_infinite_distances():
    edges = {("U", "V"): 2, ("V", "U"): 3}
    assert shortest_paths("S", edges) == {
        "S": 0,
        "U": math.inf,
        "V": math.inf,
    }


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Relaxation writes to edge weights instead of node distances",
)
@pytest.mark.parametrize(
    "source, edges, expected",
    [
        ("A", {("A", "B"): 7}, {"A": 0, "B": 7}),
        ("A", {("A", "B"): 0}, {"A": 0, "B": 0}),
        ("A", {("A", "B"): -3}, {"A": 0, "B": -3}),
        (
            "A",
            {("B", "C"): 2, ("A", "B"): 3},
            {"A": 0, "B": 3, "C": 5},
        ),
        (
            "A",
            {("A", "B"): 10, ("A", "C"): 2, ("C", "B"): 3},
            {"A": 0, "B": 5, "C": 2},
        ),
        (
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
            {"A": 0, "B": 1, "C": 3, "D": 10, "E": 5, "F": 4},
        ),
        (
            0,
            {(0, ("node", 1)): 1.25, (("node", 1), "end"): 2.5},
            {0: 0, ("node", 1): 1.25, "end": 3.75},
        ),
        (
            "A",
            {("A", "B"): 2, ("B", "A"): 1},
            {"A": 0, "B": 2},
        ),
    ],
    ids=[
        "positive-edge",
        "zero-edge",
        "negative-edge",
        "reverse-edge-order",
        "cheaper-indirect-route",
        "documented-example",
        "mixed-node-types-and-fractional-weights",
        "positive-cycle",
    ],
)
def test_minimum_path_weights(source, edges, expected):
    assert shortest_paths(source, edges) == expected


@pytest.mark.xfail(
    strict=True,
    raises=KeyError,
    reason="Node initialization omits non-source nodes with only outgoing edges",
)
def test_disconnected_edge_includes_both_unreachable_nodes():
    assert shortest_paths("S", {("U", "V"): 2}) == {
        "S": 0,
        "U": math.inf,
        "V": math.inf,
    }


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Relaxation unexpectedly mutates the caller's edge dictionary",
)
def test_input_edge_weights_are_preserved():
    edges = {("A", "B"): 2, ("B", "C"): 3}
    original = edges.copy()
    shortest_paths("A", edges)
    assert edges == original
