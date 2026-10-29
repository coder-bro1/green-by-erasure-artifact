"""Tests for the MST contract, including the current set-mutation defect."""

from itertools import combinations

import pytest

from solution import minimum_spanning_tree


def _is_spanning_tree(edges, vertices):
    if len(edges) != len(vertices) - 1:
        return False
    reached = {next(iter(vertices))}
    while True:
        expanded = reached.copy()
        for u, v in edges:
            if u in reached or v in reached:
                expanded.update((u, v))
        if expanded == reached:
            return reached == vertices
        reached = expanded


def _assert_minimum_spanning_tree(weights, result):
    """Compare against exhaustive search, independently of Kruskal's algorithm."""
    vertices = {vertex for edge in weights for vertex in edge}
    assert isinstance(result, set)
    assert result <= weights.keys()
    assert _is_spanning_tree(result, vertices)
    minimum_weight = min(
        sum(weights[edge] for edge in candidate)
        for candidate in combinations(weights, len(vertices) - 1)
        if _is_spanning_tree(candidate, vertices)
    )
    assert sum(weights[edge] for edge in result) == minimum_weight


@pytest.mark.parametrize(
    "weights",
    [{}, {(1, 1): 0}, {("a", "a"): -5}, {(1, 1): 3.5}],
    ids=["empty", "single-vertex", "negative-self-loop", "float-self-loop"],
)
def test_graph_without_connecting_edges_returns_empty_set(weights):
    original = weights.copy()
    assert minimum_spanning_tree(weights) == set()
    assert weights == original


@pytest.mark.xfail(
    strict=True,
    raises=RuntimeError,
    reason="solution.py mutates group_by_node[v] while iterating over that set",
)
@pytest.mark.parametrize(
    "weights",
    [
        {(1, 2): 7},
        {(1, 2): 10, (2, 3): 15, (3, 4): 10, (1, 4): 10},
        {(1, 2): 1, (2, 3): 2, (1, 3): 10},
        {(1, 2): -3, (2, 3): 0, (1, 3): 4},
        {(1, 2): 1, (2, 3): 1, (1, 3): 1},
        {("b", "a"): 1.5, ("c", "b"): 2.5, ("a", "c"): 9.5},
        {(1, 1): -100, (1, 2): 2, (2, 2): -10, (2, 3): 3},
        {(1, 2): 1, (3, 4): 2, (2, 3): 3, (1, 4): 10, (1, 3): 9},
    ],
    ids=[
        "single-edge",
        "docstring-example",
        "exclude-expensive-cycle-edge",
        "negative-and-zero-weights",
        "equal-weight-alternatives",
        "string-vertices-reversed-edges-and-floats",
        "ignore-self-loops",
        "merge-components",
    ],
)
def test_returns_minimum_spanning_tree_without_mutating_input(weights):
    original = weights.copy()
    try:
        result = minimum_spanning_tree(weights)
    finally:
        assert weights == original
    _assert_minimum_spanning_tree(weights, result)
