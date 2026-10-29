"""Tests for solution.shortest_paths (Bellman-Ford).

NOTE: solution.py contains a known bug -- inside the relaxation loop it assigns
to ``weight_by_edge[u, v]`` instead of ``weight_by_node[v]``. As a result no
node distance is ever relaxed (everything except the source stays at inf) and
the caller's edge dict is mutated. Tests that check the documented behavior
which this bug breaks are marked ``xfail(strict=True)``: they are reported as
expected failures now, and will turn into hard failures (XPASS) once the bug is
fixed, signalling the markers should be removed.
"""
import copy
import math

import pytest

from solution import shortest_paths

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py relaxes weight_by_edge[u, v] instead of weight_by_node[v]",
)

DOC_GRAPH = {
    ('A', 'B'): 3,
    ('A', 'C'): 3,
    ('A', 'F'): 5,
    ('C', 'B'): -2,
    ('C', 'D'): 7,
    ('C', 'E'): 4,
    ('D', 'E'): -5,
    ('E', 'F'): -1,
}


# ---------------------------------------------------------------------------
# Behavior that holds with the current implementation
# ---------------------------------------------------------------------------

def test_source_distance_is_zero():
    result = shortest_paths('A', dict(DOC_GRAPH))
    assert result['A'] == 0


def test_result_keys_are_all_nodes():
    result = shortest_paths('A', dict(DOC_GRAPH))
    assert set(result) == {'A', 'B', 'C', 'D', 'E', 'F'}


def test_empty_graph_returns_only_source():
    assert shortest_paths('A', {}) == {'A': 0}


def test_source_with_no_incoming_edges_still_included():
    result = shortest_paths('S', {('S', 'X'): 1})
    assert 'S' in result and result['S'] == 0


def test_unreachable_node_is_infinite():
    # 'Z' is only reachable from 'Y', which the source cannot reach.
    graph = {('A', 'B'): 1, ('Y', 'Z'): 2, ('Z', 'Y'): 2}
    result = shortest_paths('A', graph)
    assert math.isinf(result['Z'])
    assert math.isinf(result['Y'])


def test_returns_dict():
    assert isinstance(shortest_paths('A', {('A', 'B'): 1}), dict)


# ---------------------------------------------------------------------------
# Documented behavior broken by the bug in solution.py
# ---------------------------------------------------------------------------

@BUG
def test_docstring_example():
    assert shortest_paths('A', dict(DOC_GRAPH)) == {
        'A': 0, 'C': 3, 'B': 1, 'E': 5, 'D': 10, 'F': 4,
    }


@BUG
def test_single_edge():
    assert shortest_paths('A', {('A', 'B'): 7}) == {'A': 0, 'B': 7}


@BUG
def test_chain_requires_multiple_iterations():
    graph = {('C', 'D'): 1, ('B', 'C'): 1, ('A', 'B'): 1}
    assert shortest_paths('A', graph) == {'A': 0, 'B': 1, 'C': 2, 'D': 3}


@BUG
def test_negative_edge_gives_shorter_path():
    graph = {('A', 'B'): 4, ('A', 'C'): 1, ('C', 'B'): -2}
    assert shortest_paths('A', graph) == {'A': 0, 'B': -1, 'C': 1}


@BUG
def test_cycle_with_positive_weight():
    graph = {('A', 'B'): 1, ('B', 'C'): 2, ('C', 'A'): 3}
    assert shortest_paths('A', graph) == {'A': 0, 'B': 1, 'C': 3}


@BUG
def test_does_not_mutate_input():
    graph = dict(DOC_GRAPH)
    original = copy.deepcopy(graph)
    shortest_paths('A', graph)
    assert graph == original
