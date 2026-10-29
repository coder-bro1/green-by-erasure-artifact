"""Tests for the connected, undirected graph contract in solution.py."""

from itertools import combinations, product

import pytest

from solution import minimum_spanning_tree


def _is_connected(nodes, edges):
    """Check connectivity by walking the graph, independently of Kruskal."""
    adjacency = {node: set() for node in nodes}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    visited = set()
    pending = [next(iter(nodes))]
    while pending:
        node = pending.pop()
        if node not in visited:
            visited.add(node)
            pending.extend(adjacency[node] - visited)
    return visited == nodes


def _assert_minimum_tree(weights):
    """Compare with an exhaustive spanning-tree oracle on small graphs."""
    original = weights.copy()
    nodes = {node for edge in weights for node in edge}
    result = minimum_spanning_tree(weights)

    assert isinstance(result, set)
    assert result <= weights.keys()
    assert len(result) == len(nodes) - 1
    assert _is_connected(nodes, result)
    expected_weight = min(
        sum(weights[edge] for edge in candidate)
        for candidate in combinations(weights, len(nodes) - 1)
        if _is_connected(nodes, candidate)
    )
    assert sum(weights[edge] for edge in result) == expected_weight
    assert weights == original


@pytest.mark.parametrize(
    "weights, expected",
    [
        pytest.param(
            {(1, 2): 10, (2, 3): 15, (3, 4): 10, (1, 4): 10},
            {(1, 2), (3, 4), (1, 4)},
            id="docstring-example",
        ),
        pytest.param({("a", "b"): 7}, {("a", "b")}, id="single-edge"),
        pytest.param(
            {(0, 1): 8, (1, 2): -3, (2, 3): 0},
            {(0, 1), (1, 2), (2, 3)},
            id="already-a-tree",
        ),
        pytest.param(
            {(0, 1): 9, (1, 2): 2, (2, 0): 1},
            {(1, 2), (2, 0)},
            id="exclude-expensive-cycle-edge",
        ),
        pytest.param(
            {(0, 1): -5, (1, 2): -2, (0, 2): -1},
            {(0, 1), (1, 2)},
            id="negative-weights",
        ),
        pytest.param(
            {("a", "b"): 0.5, ("b", "c"): 1.25, ("c", "a"): 2.75},
            {("a", "b"), ("b", "c")},
            id="fractional-weights",
        ),
        pytest.param(
            {(0, 1): 1, (2, 3): 2, (1, 2): 3, (0, 3): 4},
            {(0, 1), (2, 3), (1, 2)},
            id="merge-multiple-components",
        ),
        pytest.param({("a", "a"): -10}, set(), id="single-vertex"),
        pytest.param(
            {(0, 0): -100, (1, 1): -50, (0, 1): 5},
            {(0, 1)},
            id="ignore-self-loops",
        ),
    ],
)
def test_known_minimum_spanning_trees(weights, expected):
    assert minimum_spanning_tree(weights) == expected
    _assert_minimum_tree(weights)


@pytest.mark.parametrize("reverse_order", [False, True])
def test_tied_weights_allow_any_optimal_tree(reverse_order):
    edges = list(combinations(range(4), 2))
    if reverse_order:
        edges.reverse()
    _assert_minimum_tree(dict.fromkeys(edges, 1))


def test_nodes_need_not_be_comparable():
    _assert_minimum_tree({(0, "a"): 1, ("a", (2,)): 1, ((2,), 0): 1})


def _small_connected_graphs():
    edges = list(combinations(range(4), 2))
    for choices in product((None, -2, 3), repeat=len(edges)):
        weights = {
            edge: weight
            for edge, weight in zip(edges, choices)
            if weight is not None
        }
        if _is_connected(set(range(4)), weights):
            yield weights


@pytest.mark.parametrize("weights", _small_connected_graphs())
def test_small_connected_graphs_against_exhaustive_oracle(weights):
    _assert_minimum_tree(weights)
