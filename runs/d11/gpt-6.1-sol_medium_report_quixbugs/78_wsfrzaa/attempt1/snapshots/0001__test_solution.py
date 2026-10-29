"""Tests for the connected, undirected graphs documented by solution.py."""

import pytest

from solution import minimum_spanning_tree


@pytest.mark.parametrize(
    "weights",
    [
        {(1, 2): 7},
        {(1, 2): 1, (2, 3): 2, (3, 4): 3},
        {(1, 2): 4, (1, 3): 2, (1, 4): 1},
        {(2, 1): 3, (3, 2): 1, (4, 3): 2},
        {("a", "b"): -5, ("b", "c"): -1},
        {(1, 2): 0, (2, 3): 0},
        {(1, 2): 0.25, (2, 3): 1.5},
        {(1, 2): 10**100, (2, 3): 10**101},
        {("root", 1): 1, (1, ("leaf",)): 1},
    ],
    ids=[
        "single-edge", "path", "star", "reversed-endpoints",
        "negative-weights", "zero-weights", "fractional-weights",
        "large-integers", "mixed-hashable-vertices",
    ],
)
def test_tree_keeps_every_edge(weights):
    # A connected graph that is already a tree has exactly one spanning tree.
    result = minimum_spanning_tree(weights)
    assert isinstance(result, set)
    assert result == set(weights)


@pytest.mark.parametrize(
    "weights, expected",
    [
        ({("a", "a"): 0}, set()),
        ({(1, 1): -100, (1, 2): 5}, {(1, 2)}),
        ({(1, 2): 5, (2, 2): 100}, {(1, 2)}),
    ],
    ids=["single-vertex", "cheap-self-loop", "expensive-self-loop"],
)
def test_self_loops_are_excluded(weights, expected):
    assert minimum_spanning_tree(weights) == expected


def test_input_is_not_modified_and_calls_are_independent():
    weights = {(1, 2): 3, (2, 3): 1, (3, 4): 2}
    original_items = list(weights.items())
    first = minimum_spanning_tree(weights)
    first.clear()
    assert list(weights.items()) == original_items
    assert minimum_spanning_tree(weights) == set(weights)


@pytest.mark.parametrize(
    "weights, expected",
    [
        (
            {(1, 2): 10, (2, 3): 15, (3, 4): 10, (1, 4): 10},
            {(1, 2), (3, 4), (1, 4)},
        ),
        (
            {(1, 2): 1, (1, 3): 2, (2, 3): 3},
            {(1, 2), (1, 3)},
        ),
        (
            {(1, 2): -3, (1, 3): -2, (2, 3): -1},
            {(1, 2), (1, 3)},
        ),
        (
            {(2, 3): 3, (1, 3): 2, (1, 2): 1},
            {(1, 2), (1, 3)},
        ),
    ],
    ids=["docstring-example", "triangle", "negative-cycle", "unsorted-input"],
)
def test_unique_minimum_spanning_tree(weights, expected):
    assert minimum_spanning_tree(weights) == expected


def test_equal_weights_allow_any_minimum_spanning_tree():
    weights = {(1, 2): 1, (2, 3): 1, (1, 3): 1}
    result = minimum_spanning_tree(weights)
    # Any pair of edges in this triangle is a valid minimum spanning tree.
    assert result <= set(weights)
    assert len(result) == 2
    assert {vertex for edge in result for vertex in edge} == {1, 2, 3}
    assert sum(weights[edge] for edge in result) == 2
