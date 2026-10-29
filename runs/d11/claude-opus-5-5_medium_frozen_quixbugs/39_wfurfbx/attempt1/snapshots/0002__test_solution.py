import sys

import pytest

from node import Node
from solution import depth_first_search


def make(value, successors=None):
    # Always pass an explicit list: Node's default `successors=[]` is a shared
    # mutable default.
    return Node(value, successors=list(successors or []))


def test_start_is_goal():
    a = make("a")
    assert depth_first_search(a, a) is True


def test_direct_successor():
    b = make("b")
    a = make("a", [b])
    assert depth_first_search(a, b) is True


def test_unreachable_isolated_nodes():
    a = make("a")
    b = make("b")
    assert depth_first_search(a, b) is False


def test_long_chain():
    nodes = [make(i) for i in range(50)]
    for cur, nxt in zip(nodes, nodes[1:]):
        cur.successors = [nxt]
    assert depth_first_search(nodes[0], nodes[-1]) is True
    assert depth_first_search(nodes[-1], nodes[0]) is False


def test_edges_are_directed():
    b = make("b")
    a = make("a", [b])
    assert depth_first_search(b, a) is False


def test_branching_goal_in_later_branch():
    goal = make("goal")
    d = make("d")
    c = make("c", [goal])
    b = make("b", [d])
    a = make("a", [b, c])
    assert depth_first_search(a, goal) is True


def test_branching_goal_not_reachable():
    goal = make("goal")
    c = make("c")
    b = make("b")
    a = make("a", [b, c])
    assert depth_first_search(a, goal) is False


def test_diamond_dag():
    d = make("d")
    b = make("b", [d])
    c = make("c", [d])
    a = make("a", [b, c])
    assert depth_first_search(a, d) is True
    assert depth_first_search(b, c) is False


def test_identity_not_equality():
    # Goal is matched by identity, so a different node with the same value
    # does not count.
    goal = make("x")
    lookalike = make("x")
    a = make("a", [lookalike])
    assert depth_first_search(a, goal) is False


def test_cycle_with_reachable_goal():
    # The goal is found before the search loops back around.
    goal = make("goal")
    a = make("a")
    b = make("b", [a, goal])
    a.successors = [b]
    assert depth_first_search(a, goal) is True


def test_self_loop_goal_found_first():
    goal = make("goal")
    a = make("a")
    a.successors = [goal, a]
    assert depth_first_search(a, goal) is True


@pytest.mark.xfail(
    raises=RecursionError,
    strict=True,
    reason="Known bug in solution.py: nodes are never added to nodesvisited, "
    "so a cycle that can't reach the goal recurses forever.",
)
def test_cycle_with_unreachable_goal_terminates():
    goal = make("goal")
    a = make("a")
    b = make("b", [a])
    a.successors = [b]
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(500)
    try:
        assert depth_first_search(a, goal) is False
    finally:
        sys.setrecursionlimit(old)
