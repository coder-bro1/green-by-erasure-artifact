"""Tests for supported cases and characterization of current limitations."""

from math import inf

import pytest

from node import Node
from solution import get, insert_or_update, shortest_path_length


def make_node(value):
    # Supply fresh lists because Node's constructor has shared mutable defaults.
    return Node(
        value=value,
        successors=[],
        predecessors=[],
        incoming_nodes=[],
        outgoing_nodes=[],
    )


@pytest.mark.parametrize("with_edge", [False, True])
def test_start_is_goal_returns_zero(with_edge):
    start, other = make_node("start"), make_node("other")
    edges = {}
    if with_edge:
        start.successors.append(other)
        edges[start, other] = 3
    assert shortest_path_length(edges, start, start) == 0


@pytest.mark.parametrize("weight", [1, 7, 1.25, 10**12])
def test_single_edge_returns_its_weight(weight):
    start, goal = make_node("start"), make_node("goal")
    start.successors.append(goal)
    assert shortest_path_length({(start, goal): weight}, start, goal) == weight


def test_distinct_isolated_nodes_are_unreachable():
    assert shortest_path_length({}, make_node("start"), make_node("goal")) == inf


def test_edges_are_directed():
    start, goal = make_node("start"), make_node("goal")
    goal.successors.append(start)
    assert shortest_path_length({(goal, start): 4}, start, goal) == inf


def test_cycle_terminates_when_goal_is_unreachable():
    start, other, goal = (make_node(value) for value in ("start", "other", "goal"))
    start.successors.append(other)
    other.successors.append(start)
    assert shortest_path_length({(start, other): 2, (other, start): 3}, start, goal) == inf


def test_goal_is_found_after_cheaper_dead_end():
    start, dead_end, goal = (make_node(value) for value in ("start", "dead", "goal"))
    start.successors.extend([goal, dead_end])
    assert shortest_path_length({(start, goal): 9, (start, dead_end): 2}, start, goal) == 9


@pytest.mark.parametrize("distance", [0, 3, 2.5])
def test_get_returns_distance_of_matching_node(distance):
    first, wanted = make_node("first"), make_node("wanted")
    assert get([(1, first), (distance, wanted)], wanted) == distance


def test_get_returns_zero_for_missing_node():
    assert get([(3, make_node("present"))], make_node("missing")) == 0
    assert get([], make_node("missing")) == 0


def test_get_uses_equality_and_does_not_mutate_heap():
    heap = [(2, ["first"]), (5, ["wanted"])]
    before = heap.copy()
    assert get(heap, ["wanted"]) == 5
    assert heap == before


def test_insert_into_empty_heap():
    heap = []
    node = make_node("new")
    assert insert_or_update(heap, (4, node)) is None
    assert heap == [(4, node)]


def test_insert_new_node_preserves_existing_entries():
    existing, new = make_node("existing"), make_node("new")
    heap = [(8, existing)]
    assert insert_or_update(heap, (2, new)) is None
    assert heap == [(2, new), (8, existing)]


def test_update_replaces_entry_without_duplicate():
    root, other = make_node("root"), make_node("other")
    heap = [(3, root), (8, other)]
    assert insert_or_update(heap, (1, root)) is None
    assert heap == [(1, root), (8, other)]


def test_update_uses_equality():
    heap = [(3, ["same"])]
    assert insert_or_update(heap, (2, ["same"])) is None
    assert heap == [(2, ["same"])]


def test_current_multihop_behavior_omits_accumulated_distance():
    """Characterize the existing bug: this path should have length 12."""
    start, middle, goal = (make_node(value) for value in ("start", "middle", "goal"))
    start.successors.append(middle)
    middle.successors.append(goal)
    assert shortest_path_length({(start, middle): 5, (middle, goal): 7}, start, goal) == 7


def test_current_update_behavior_does_not_restore_heap_order():
    """Characterize the existing bug: the updated minimum stays at index 1."""
    root, other = make_node("root"), make_node("other")
    heap = [(3, root), (8, other)]
    insert_or_update(heap, (1, other))
    assert heap == [(3, root), (1, other)]
