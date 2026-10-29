"""Tests for solution.shortest_path_lengths (Floyd-Warshall).

NOTE: solution.py contains a known bug. The relaxation step reads
    length_by_path[i, k] + length_by_path[j, k]
instead of the correct
    length_by_path[i, k] + length_by_path[k, j]
The result is still correct for symmetric (undirected) graphs, but wrong for
general directed graphs. Tests that exercise the directed case are marked
xfail(strict=True): they document the correct expected behavior and will
start failing (XPASS -> error) once the bug is fixed, prompting removal of
the marker.
"""
import math

import pytest

from solution import shortest_path_lengths

INF = float("inf")

directed_bug = pytest.mark.xfail(
    strict=True,
    reason="solution.py uses length_by_path[j, k] instead of [k, j] in relaxation",
)


def reference_floyd_warshall(n, edges):
    d = {(i, j): (0 if i == j else INF) for i in range(n) for j in range(n)}
    for (u, v), w in edges.items():
        d[u, v] = min(d[u, v], w) if u != v else min(0, w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i, k] + d[k, j] < d[i, j]:
                    d[i, j] = d[i, k] + d[k, j]
    return d


def as_full_matrix(result, n):
    return {(i, j): result[i, j] for i in range(n) for j in range(n)}


def symmetric(edges):
    out = dict(edges)
    out.update({(v, u): w for (u, v), w in edges.items()})
    return out


# --- Behaviour that is correct in the current implementation -----------------

def test_empty_graph():
    assert dict(shortest_path_lengths(0, {})) == {}


def test_single_node_distance_to_self_is_zero():
    result = shortest_path_lengths(1, {})
    assert result[0, 0] == 0


def test_no_edges_unreachable_is_infinite():
    result = shortest_path_lengths(3, {})
    for i in range(3):
        for j in range(3):
            assert result[i, j] == (0 if i == j else INF)


def test_missing_key_defaults_to_infinity():
    result = shortest_path_lengths(2, {})
    assert math.isinf(result[5, 7])


def test_single_directed_edge():
    result = shortest_path_lengths(2, {(0, 1): 4})
    assert result[0, 1] == 4
    assert result[1, 0] == INF
    assert result[0, 0] == 0
    assert result[1, 1] == 0


def test_input_dict_not_mutated():
    edges = {(0, 1): 3, (1, 0): 3}
    snapshot = dict(edges)
    shortest_path_lengths(2, edges)
    assert edges == snapshot


def test_undirected_triangle_takes_shorter_two_hop_route():
    edges = symmetric({(0, 1): 1, (1, 2): 1, (0, 2): 5})
    result = shortest_path_lengths(3, edges)
    assert result[0, 2] == 2
    assert result[2, 0] == 2


def test_undirected_path_graph():
    edges = symmetric({(0, 1): 2, (1, 2): 3, (2, 3): 4})
    result = shortest_path_lengths(4, edges)
    assert result[0, 3] == 9
    assert result[3, 0] == 9
    assert result[1, 3] == 7


def test_undirected_disconnected_components():
    edges = symmetric({(0, 1): 1, (2, 3): 1})
    result = shortest_path_lengths(4, edges)
    assert result[0, 1] == 1
    assert result[0, 2] == INF
    assert result[3, 1] == INF


def test_undirected_matches_reference_on_larger_graph():
    edges = symmetric({
        (0, 1): 7, (0, 2): 9, (0, 5): 14, (1, 2): 10, (1, 3): 15,
        (2, 3): 11, (2, 5): 2, (3, 4): 6, (4, 5): 9,
    })
    n = 6
    assert as_full_matrix(shortest_path_lengths(n, edges), n) == \
        reference_floyd_warshall(n, edges)


def test_floats_supported():
    edges = symmetric({(0, 1): 0.5, (1, 2): 0.25})
    result = shortest_path_lengths(3, edges)
    assert result[0, 2] == pytest.approx(0.75)


def test_negative_symmetric_edge_weights_without_cycle_effect():
    # Directed edges only one way through 1 so no negative cycle is formed,
    # and the path 0->1->2 uses entries the buggy indexing also reads correctly.
    result = shortest_path_lengths(2, {(0, 1): -3})
    assert result[0, 1] == -3


# --- Directed-graph behaviour (exposes the bug) -------------------------------

@directed_bug
def test_directed_chain_two_hops():
    result = shortest_path_lengths(3, {(0, 1): 1, (1, 2): 1})
    assert result[0, 2] == 2


@directed_bug
def test_directed_shortcut_via_intermediate():
    result = shortest_path_lengths(3, {(0, 1): 1, (1, 2): 1, (0, 2): 10})
    assert result[0, 2] == 2


@directed_bug
def test_directed_unreachable_in_reverse_direction():
    result = shortest_path_lengths(3, {(0, 1): 1, (1, 2): 1})
    # Correct: 2 cannot reach 0, and 0 reaches 2 at cost 2.
    assert result[2, 0] == INF
    assert result[0, 2] == 2


@directed_bug
def test_directed_negative_edges_no_negative_cycle():
    # Classic QuixBugs case.
    edges = {
        (0, 2): 3, (0, 5): -2, (5, 3): -1, (5, 4): -1,
        (2, 1): -2, (1, 4): -2, (4, 3): 3,
    }
    result = shortest_path_lengths(6, edges)
    assert result[0, 1] == 1
    assert result[0, 4] == -3
    assert result[0, 3] == -3


@directed_bug
def test_directed_matches_reference():
    edges = {(0, 1): 3, (1, 2): 4, (2, 3): 5, (3, 0): 1, (0, 2): 10}
    n = 4
    assert as_full_matrix(shortest_path_lengths(n, edges), n) == \
        reference_floyd_warshall(n, edges)
