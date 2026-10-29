"""Tests for the directed all-pairs shortest-path contract in solution.py."""

from math import inf

import pytest

from solution import shortest_path_lengths


@pytest.mark.parametrize("n", [0, 1, 4])
def test_graph_without_edges(n):
    expected = {
        (i, j): 0 if i == j else inf
        for i in range(n)
        for j in range(n)
    }
    assert dict(shortest_path_lengths(n, {})) == expected


def test_zero_length_self_loop():
    assert dict(shortest_path_lengths(1, {(0, 0): 0})) == {(0, 0): 0}


def test_symmetric_graph_chooses_shorter_indirect_route():
    edges = {
        (0, 1): 2, (1, 0): 2,
        (1, 2): 3, (2, 1): 3,
        (0, 2): 10, (2, 0): 10,
    }
    expected = {
        (0, 0): 0, (0, 1): 2, (0, 2): 5,
        (1, 0): 2, (1, 1): 0, (1, 2): 3,
        (2, 0): 5, (2, 1): 3, (2, 2): 0,
    }
    assert dict(shortest_path_lengths(3, edges)) == expected


def test_disconnected_components_with_fractional_weights():
    edges = {(0, 1): 1.25, (1, 0): 1.25, (2, 3): 2.5, (3, 2): 2.5}
    expected = {(i, j): 0 if i == j else inf for i in range(4) for j in range(4)}
    expected.update(edges)
    assert dict(shortest_path_lengths(4, edges)) == expected


def test_does_not_mutate_input_edges():
    edges = {(0, 1): 4, (1, 2): -1}
    original = edges.copy()
    shortest_path_lengths(3, edges)
    assert edges == original


@pytest.mark.parametrize("weight", [7, 0])
def test_single_directed_edge(weight):
    expected = {(0, 0): 0, (0, 1): weight, (1, 0): inf, (1, 1): 0}
    assert dict(shortest_path_lengths(2, {(0, 1): weight})) == expected


def test_asymmetric_bidirectional_edges():
    expected = {(0, 0): 0, (0, 1): 2, (1, 0): 9, (1, 1): 0}
    assert dict(shortest_path_lengths(2, {(0, 1): 2, (1, 0): 9})) == expected


def test_directed_chain_beats_expensive_direct_edge():
    edges = {(0, 1): 2, (1, 2): 3, (0, 2): 10}
    expected = {
        (0, 0): 0, (0, 1): 2, (0, 2): 5,
        (1, 0): inf, (1, 1): 0, (1, 2): 3,
        (2, 0): inf, (2, 1): inf, (2, 2): 0,
    }
    assert dict(shortest_path_lengths(3, edges)) == expected


def test_negative_edge_without_negative_cycle():
    # An acyclic graph satisfies the documented no-negative-cycles precondition.
    edges = {(0, 1): 4, (1, 2): -2, (0, 2): 8}
    expected = {
        (0, 0): 0, (0, 1): 4, (0, 2): 2,
        (1, 0): inf, (1, 1): 0, (1, 2): -2,
        (2, 0): inf, (2, 1): inf, (2, 2): 0,
    }
    assert dict(shortest_path_lengths(3, edges)) == expected


def test_positive_self_loop_keeps_zero_distance_to_self():
    assert dict(shortest_path_lengths(1, {(0, 0): 5})) == {(0, 0): 0}
