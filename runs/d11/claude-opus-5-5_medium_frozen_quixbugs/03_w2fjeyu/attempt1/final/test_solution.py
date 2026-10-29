"""Tests for solution.minimum_spanning_tree (Kruskal's algorithm).

NOTE: solution.py currently contains a bug in its union step:

    for node in group_by_node[v]:
        group_by_node[node].update(group_by_node[u])

When node == v this mutates the set being iterated, raising
``RuntimeError: Set changed size during iteration`` for any graph with at
least one edge (the docstring example included). The intended line is
``group_by_node[node] = group_by_node[u]``.

Tests that exercise that path are marked ``xfail(strict=True,
raises=RuntimeError)``: they encode the documented behaviour, currently fail
for exactly that reason, and will turn into hard failures (XPASS) once the
bug is fixed so the markers can be removed.
"""

from itertools import combinations

import pytest

from solution import minimum_spanning_tree


known_bug = pytest.mark.xfail(
    strict=True,
    raises=RuntimeError,
    reason="solution.py mutates a set while iterating over it in the union step",
)


def total_weight(edges, weight_by_edge):
    return sum(weight_by_edge[e] for e in edges)


def is_spanning_tree(edges, weight_by_edge):
    nodes = {n for e in weight_by_edge for n in e}
    if len(edges) != max(len(nodes) - 1, 0):
        return False
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False  # cycle
        parent[ru] = rv
    return len({find(n) for n in nodes}) <= 1


def brute_force_mst_weight(weight_by_edge):
    nodes = {n for e in weight_by_edge for n in e}
    k = len(nodes) - 1
    best = None
    for subset in combinations(weight_by_edge, k):
        if is_spanning_tree(set(subset), weight_by_edge):
            w = total_weight(subset, weight_by_edge)
            best = w if best is None else min(best, w)
    return best


# --- Cases that currently pass ------------------------------------------------

def test_empty_graph_returns_empty_set():
    assert minimum_spanning_tree({}) == set()


def test_returns_a_set():
    assert isinstance(minimum_spanning_tree({}), set)


def test_does_not_mutate_input_empty():
    g = {}
    minimum_spanning_tree(g)
    assert g == {}


# --- Cases blocked by the bug in solution.py ----------------------------------

@known_bug
def test_docstring_example():
    g = {(1, 2): 10, (2, 3): 15, (3, 4): 10, (1, 4): 10}
    assert minimum_spanning_tree(g) == {(1, 2), (3, 4), (1, 4)}


@known_bug
def test_single_edge():
    assert minimum_spanning_tree({(1, 2): 5}) == {(1, 2)}


@known_bug
def test_path_graph_keeps_all_edges():
    g = {(1, 2): 3, (2, 3): 1, (3, 4): 2}
    assert minimum_spanning_tree(g) == set(g)


@known_bug
def test_triangle_drops_heaviest_edge():
    g = {(1, 2): 1, (2, 3): 2, (1, 3): 3}
    assert minimum_spanning_tree(g) == {(1, 2), (2, 3)}


@known_bug
def test_star_graph():
    g = {(0, 1): 4, (0, 2): 5, (0, 3): 6}
    assert minimum_spanning_tree(g) == set(g)


@known_bug
def test_string_nodes():
    g = {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 5}
    assert minimum_spanning_tree(g) == {("a", "b"), ("b", "c")}


@known_bug
def test_negative_weights():
    g = {(1, 2): -5, (2, 3): -1, (1, 3): 0}
    assert minimum_spanning_tree(g) == {(1, 2), (2, 3)}


@known_bug
def test_does_not_mutate_input():
    g = {(1, 2): 1, (2, 3): 2, (1, 3): 3}
    snapshot = dict(g)
    minimum_spanning_tree(g)
    assert g == snapshot


@known_bug
@pytest.mark.parametrize(
    "g",
    [
        {(1, 2): 7, (1, 3): 8, (2, 3): 11, (2, 4): 2, (3, 4): 6, (3, 5): 4,
         (4, 5): 9, (4, 6): 1, (5, 6): 3},
        {(1, 2): 1, (1, 3): 1, (1, 4): 1, (2, 3): 1, (2, 4): 1, (3, 4): 1},
        {(1, 2): 6, (1, 3): 1, (1, 4): 5, (2, 3): 5, (2, 5): 3, (3, 4): 5,
         (3, 5): 6, (3, 6): 4, (4, 6): 2, (5, 6): 6},
    ],
)
def test_result_is_minimum_spanning_tree(g):
    result = minimum_spanning_tree(g)
    assert result <= set(g)
    assert is_spanning_tree(result, g)
    assert total_weight(result, g) == brute_force_mst_weight(g)


# --- Sanity checks for the test helpers themselves ----------------------------

def test_helper_is_spanning_tree():
    g = {(1, 2): 1, (2, 3): 2, (1, 3): 3}
    assert is_spanning_tree({(1, 2), (2, 3)}, g)
    assert not is_spanning_tree({(1, 2)}, g)
    assert not is_spanning_tree({(1, 2), (2, 3), (1, 3)}, g)


def test_helper_brute_force_weight():
    g = {(1, 2): 10, (2, 3): 15, (3, 4): 10, (1, 4): 10}
    assert brute_force_mst_weight(g) == 30
