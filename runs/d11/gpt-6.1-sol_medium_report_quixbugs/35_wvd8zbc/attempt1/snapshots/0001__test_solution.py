"""Tests for the documented minimum-weight paths contract."""

from math import inf

import pytest

from solution import shortest_paths


def test_docstring_example():
    edges = {
        ("A", "B"): 3,
        ("A", "C"): 3,
        ("A", "F"): 5,
        ("C", "B"): -2,
        ("C", "D"): 7,
        ("C", "E"): 4,
        ("D", "E"): -5,
        ("E", "F"): -1,
    }
    assert shortest_paths("A", edges) == {
        "A": 0, "B": 1, "C": 3, "D": 10, "E": 5, "F": 4,
    }


@pytest.mark.parametrize(
    "source, edges, expected",
    [
        pytest.param("A", {}, {"A": 0}, id="empty-graph"),
        pytest.param("A", {("A", "B"): 7}, {"A": 0, "B": 7}, id="single-edge"),
        pytest.param("A", {("A", "B"): -7}, {"A": 0, "B": -7}, id="negative-edge"),
        pytest.param(
            "A", {("A", "B"): 0, ("B", "C"): 0},
            {"A": 0, "B": 0, "C": 0}, id="zero-weight-path",
        ),
        pytest.param(
            "A", {("C", "D"): 3, ("B", "C"): -2, ("A", "B"): 4},
            {"A": 0, "B": 4, "C": 2, "D": 5}, id="reverse-edge-order",
        ),
        pytest.param(
            "A", {("A", "B"): 8, ("A", "C"): 2, ("C", "B"): 1},
            {"A": 0, "B": 3, "C": 2}, id="cheaper-indirect-path",
        ),
        pytest.param(
            "A", {("A", "B"): 2, ("B", "C"): 3, ("C", "A"): 4},
            {"A": 0, "B": 2, "C": 5}, id="positive-cycle",
        ),
        pytest.param(
            "A", {("A", "B"): 2, ("B", "C"): -2, ("C", "A"): 0},
            {"A": 0, "B": 2, "C": 0}, id="zero-total-cycle",
        ),
        pytest.param("A", {("A", "A"): 5}, {"A": 0}, id="positive-self-loop"),
        pytest.param("A", {("A", "A"): 0}, {"A": 0}, id="zero-self-loop"),
        pytest.param(
            "A", {("A", "B"): 2, ("X", "Y"): -3, ("Y", "X"): 4},
            {"A": 0, "B": 2, "X": inf, "Y": inf}, id="unreachable-component",
        ),
        pytest.param(
            "S", {("X", "Y"): 1, ("Y", "X"): 1},
            {"S": 0, "X": inf, "Y": inf}, id="source-outside-edges",
        ),
        pytest.param(
            0, {(0, "B"): 2, ("B", (1, 2)): -1},
            {0: 0, "B": 2, (1, 2): 1}, id="mixed-hashable-node-ids",
        ),
        pytest.param(
            "A", {("A", "B"): 1.5, ("B", "C"): -0.25},
            {"A": 0, "B": 1.5, "C": 1.25}, id="fractional-weights",
        ),
    ],
)
def test_shortest_paths(source, edges, expected):
    assert shortest_paths(source, edges) == expected


def test_input_edges_are_not_modified():
    edges = {("A", "B"): 4, ("B", "C"): -2, ("A", "C"): 9}
    original = edges.copy()
    assert shortest_paths("A", edges) == {"A": 0, "B": 4, "C": 2}
    assert edges == original


@pytest.mark.parametrize(
    "edges, expected",
    [
        pytest.param(
            {("X", "A"): 1}, {"A": 0, "X": inf},
            id="unreachable-origin-pointing-to-source",
        ),
        pytest.param(
            {("A", "B"): 2, ("X", "B"): 1},
            {"A": 0, "B": 2, "X": inf},
            id="unreachable-origin-pointing-to-reachable-node",
        ),
    ],
)
def test_nodes_that_only_appear_as_edge_origins(edges, expected):
    assert shortest_paths("A", edges) == expected
