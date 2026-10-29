import pytest

from node import Node
from solution import detect_cycle


def build_list(n, cycle_to=None):
    """Build a linked list of n nodes (values 0..n-1).

    If cycle_to is an index, the last node links back to that node.
    Returns the head node.
    """
    nodes = [Node(value=i) for i in range(n)]
    for a, b in zip(nodes, nodes[1:]):
        a.successor = b
    if cycle_to is not None:
        nodes[-1].successor = nodes[cycle_to]
    return nodes[0]


# --- Cyclic lists: should return True ---------------------------------------

def test_single_node_self_loop():
    head = build_list(1, cycle_to=0)
    assert detect_cycle(head) is True


def test_two_node_cycle():
    head = build_list(2, cycle_to=0)
    assert detect_cycle(head) is True


@pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 10, 101])
def test_full_cycle_back_to_head(n):
    assert detect_cycle(build_list(n, cycle_to=0)) is True


@pytest.mark.parametrize("n,cycle_to", [
    (5, 2), (5, 4), (6, 1), (6, 5), (10, 3), (10, 9), (100, 50),
])
def test_cycle_into_middle_or_tail(n, cycle_to):
    assert detect_cycle(build_list(n, cycle_to=cycle_to)) is True


def test_does_not_mutate_list():
    head = build_list(5, cycle_to=2)
    before = []
    node = head
    for _ in range(5):
        before.append((node, node.successor))
        node = node.successor
    detect_cycle(head)
    node = head
    for orig, succ in before:
        assert node is orig and node.successor is succ
        node = node.successor


# --- Acyclic lists: should return False -------------------------------------

def test_single_node_no_cycle():
    assert detect_cycle(build_list(1)) is False


@pytest.mark.parametrize("n", [3, 5, 7, 11, 101])
def test_odd_length_acyclic(n):
    assert detect_cycle(build_list(n)) is False


# --- Known bug in solution.py -----------------------------------------------
# For acyclic lists of even length, the hare jumps to None and the next
# `hare.successor` access raises AttributeError instead of returning False.
# Correct check: `if hare is None or hare.successor is None: return False`.
# These tests assert the correct behavior and are marked strict xfail so the
# suite flags it (XPASS -> failure) once solution.py is fixed.

@pytest.mark.xfail(raises=AttributeError, strict=True,
                   reason="solution.py bug: even-length acyclic list crashes")
@pytest.mark.parametrize("n", [2, 4, 6, 10, 100])
def test_even_length_acyclic(n):
    assert detect_cycle(build_list(n)) is False


@pytest.mark.xfail(raises=AttributeError, strict=True,
                   reason="solution.py does not handle an empty list (None head)")
def test_empty_list():
    assert detect_cycle(None) is False
