"""Tests for solution.shortest_path_length (Dijkstra).

The expected values below are the *correct* shortest-path lengths per the
docstring. solution.py contains a known defect: when relaxing an edge it adds
the edge length to the neighbour's current heap distance (``get(...)``, which
is 0 for an unseen node) instead of to the popped node's ``distance``. As a
result any path longer than one edge is mis-measured. Those cases are marked
``xfail(strict=True)`` so the suite passes today and will flag (XPASS -> fail)
once the bug is fixed, prompting removal of the markers.
"""
import pytest

from node import Node
from solution import shortest_path_length, get, insert_or_update

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py adds edge length to neighbour's heap distance instead of popped node's distance",
)


def make_graph(edges, names):
    """Build Nodes from {(u, v): length} using names; returns (nodes, length_by_edge)."""
    nodes = {n: Node(n, successors=[]) for n in names}
    length_by_edge = {}
    for (u, v), length in edges.items():
        nodes[u].successors.append(nodes[v])
        length_by_edge[nodes[u], nodes[v]] = length
    return nodes, length_by_edge


# ---------------------------------------------------------------- correct today

def test_start_is_goal_returns_zero():
    nodes, lengths = make_graph({("a", "b"): 5}, "ab")
    assert shortest_path_length(lengths, nodes["a"], nodes["a"]) == 0


def test_isolated_start_is_goal():
    a = Node("a", successors=[])
    assert shortest_path_length({}, a, a) == 0


def test_single_edge():
    nodes, lengths = make_graph({("a", "b"): 7}, "ab")
    assert shortest_path_length(lengths, nodes["a"], nodes["b"]) == 7


def test_picks_shorter_of_two_direct_edges_to_different_nodes():
    nodes, lengths = make_graph({("a", "b"): 3, ("a", "c"): 9}, "abc")
    assert shortest_path_length(lengths, nodes["a"], nodes["b"]) == 3
    assert shortest_path_length(lengths, nodes["a"], nodes["c"]) == 9


def test_unreachable_goal_returns_inf():
    nodes, lengths = make_graph({("a", "b"): 1}, "abc")
    assert shortest_path_length(lengths, nodes["a"], nodes["c"]) == float("inf")


def test_edges_are_directed():
    nodes, lengths = make_graph({("a", "b"): 1}, "ab")
    assert shortest_path_length(lengths, nodes["b"], nodes["a"]) == float("inf")


def test_cycle_back_to_start_does_not_loop_forever():
    nodes, lengths = make_graph({("a", "b"): 2, ("b", "a"): 2}, "abc")
    assert shortest_path_length(lengths, nodes["a"], nodes["c"]) == float("inf")


def test_float_edge_length():
    nodes, lengths = make_graph({("a", "b"): 2.5}, "ab")
    assert shortest_path_length(lengths, nodes["a"], nodes["b"]) == pytest.approx(2.5)


# ------------------------------------------------------------- helper functions

def test_get_returns_distance_of_present_node():
    a, b = Node("a"), Node("b")
    assert get([(4, a), (9, b)], b) == 9


def test_get_returns_zero_for_missing_node():
    a, b = Node("a"), Node("b")
    assert get([(4, a)], b) == 0
    assert get([], a) == 0


def test_insert_or_update_inserts_new_node():
    a = Node("a")
    heap = []
    assert insert_or_update(heap, (3, a)) is None
    assert heap == [(3, a)]


def test_insert_or_update_replaces_existing_node():
    a, b = Node("a"), Node("b")
    heap = [(1, a), (5, b)]
    insert_or_update(heap, (2, b))
    assert heap == [(1, a), (2, b)]


# ------------------------------------------- correct expectations, currently fail

@BUG
def test_two_edge_chain():
    nodes, lengths = make_graph({("a", "b"): 3, ("b", "c"): 4}, "abc")
    assert shortest_path_length(lengths, nodes["a"], nodes["c"]) == 7


@BUG
def test_indirect_path_shorter_than_direct_edge():
    nodes, lengths = make_graph({("a", "b"): 1, ("a", "c"): 10, ("b", "c"): 1}, "abc")
    assert shortest_path_length(lengths, nodes["a"], nodes["c"]) == 2


@BUG
def test_classic_quixbugs_graph():
    edges = {
        ("A", "B"): 3, ("A", "C"): 3, ("A", "F"): 5,
        ("C", "B"): -2 + 4,  # keep positive per precondition
        ("C", "D"): 7, ("C", "E"): 2,
        ("D", "E"): 2, ("E", "F"): 1,
    }
    # Correct answers: A->C->E->F = 6 vs A->F = 5 -> 5; A->C->D = 10; A->C->E = 5
    nodes, lengths = make_graph(edges, "ABCDEF")
    assert shortest_path_length(lengths, nodes["A"], nodes["D"]) == 10
    assert shortest_path_length(lengths, nodes["A"], nodes["E"]) == 5
    assert shortest_path_length(lengths, nodes["A"], nodes["F"]) == 5
