import pytest

from node import Node
from solution import breadth_first_search


UNREACHABLE_BUG = (
    "solution.py loops with `while True` instead of `while queue`, so an "
    "exhausted queue raises IndexError instead of returning False"
)


def make(value, successors=None):
    # Always pass a fresh list: Node uses a shared mutable default.
    return Node(value, successors=list(successors or []))


def test_start_is_goal():
    a = make("a")
    assert breadth_first_search(a, a) is True


def test_direct_successor():
    b = make("b")
    a = make("a", [b])
    assert breadth_first_search(a, b) is True


def test_long_chain():
    nodes = [make(i) for i in range(50)]
    for cur, nxt in zip(nodes, nodes[1:]):
        cur.successors = [nxt]
    assert breadth_first_search(nodes[0], nodes[-1]) is True


def test_branching_graph():
    #      station1
    #     /    |    \
    #   s2    s3    s4
    #   |      |   /  \
    #   s5    s6  s7  s8 (goal)
    s8 = make("s8")
    s7 = make("s7")
    s6 = make("s6")
    s5 = make("s5")
    s4 = make("s4", [s7, s8])
    s3 = make("s3", [s6])
    s2 = make("s2", [s5])
    s1 = make("s1", [s2, s3, s4])
    assert breadth_first_search(s1, s8) is True


def test_cycle_with_reachable_goal():
    a, b, c = make("a"), make("b"), make("c")
    goal = make("goal")
    a.successors = [b]
    b.successors = [c, a]
    c.successors = [a, goal]
    assert breadth_first_search(a, goal) is True


def test_self_loop_then_goal():
    goal = make("goal")
    a = make("a")
    a.successors = [a, goal]
    assert breadth_first_search(a, goal) is True


def test_diamond_with_shared_node():
    goal = make("goal")
    d = make("d", [goal])
    b = make("b", [d])
    c = make("c", [d])
    a = make("a", [b, c])
    assert breadth_first_search(a, goal) is True


def test_identity_not_equality():
    # Goal is matched by identity; a different node with the same value
    # is not the goal, but the real goal is still found.
    goal = make("x")
    lookalike = make("x")
    a = make("a", [lookalike, goal])
    assert breadth_first_search(a, goal) is True


def test_edges_are_directed():
    # b -> a exists, but we search from a to b: only a -> c exists.
    a, b, c = make("a"), make("b"), make("c")
    b.successors = [a]
    a.successors = [c]
    goal = make("goal")
    c.successors = [goal]
    assert breadth_first_search(a, goal) is True


# --- Unreachable goal: documents a known bug in solution.py -----------------

@pytest.mark.xfail(raises=IndexError, strict=True, reason=UNREACHABLE_BUG)
def test_unreachable_isolated_nodes():
    a, b = make("a"), make("b")
    assert breadth_first_search(a, b) is False


@pytest.mark.xfail(raises=IndexError, strict=True, reason=UNREACHABLE_BUG)
def test_unreachable_in_disconnected_component():
    a, b = make("a"), make("b")
    c, d = make("c"), make("d")
    a.successors = [b]
    c.successors = [d]
    assert breadth_first_search(a, d) is False


@pytest.mark.xfail(raises=IndexError, strict=True, reason=UNREACHABLE_BUG)
def test_unreachable_against_edge_direction():
    a, b = make("a"), make("b")
    b.successors = [a]
    assert breadth_first_search(a, b) is False


@pytest.mark.xfail(raises=IndexError, strict=True, reason=UNREACHABLE_BUG)
def test_unreachable_with_cycle_terminates():
    a, b, c = make("a"), make("b"), make("c")
    a.successors = [b]
    b.successors = [c]
    c.successors = [a]
    goal = make("goal")
    assert breadth_first_search(a, goal) is False


def test_current_behavior_on_unreachable_raises_indexerror():
    # Pins the actual current behavior so a fix is noticed.
    a, b = make("a"), make("b")
    with pytest.raises(IndexError):
        breadth_first_search(a, b)
