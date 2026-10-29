"""Tests for solution.reverse_linked_list.

NOTE: solution.py contains a known bug -- the loop never executes
``prevnode = node``, so the function always returns ``None`` and every node
after the original head is detached. Tests that check the documented
behaviour are marked ``xfail(strict=True)``: they document the bug, and will
start failing loudly (XPASS -> error) once the bug is fixed, signalling that
the markers should be removed.
"""
import pytest

from node import Node
from solution import reverse_linked_list

BUG = "solution.py never assigns prevnode = node, so it always returns None"


def build(values):
    """Build a singly-linked list from values; return (head, nodes)."""
    nodes = [Node(value=v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.successor = b
    if nodes:
        nodes[-1].successor = None
    return (nodes[0] if nodes else None), nodes


def to_list(head, limit=1000):
    out = []
    while head is not None:
        out.append(head.value)
        head = head.successor
        if len(out) > limit:
            raise AssertionError("cycle detected")
    return out


# --- Behaviour that holds for the current implementation -------------------

def test_empty_list_returns_none():
    assert reverse_linked_list(None) is None


def test_original_head_successor_becomes_none():
    head, nodes = build([1, 2, 3])
    reverse_linked_list(head)
    assert nodes[0].successor is None


def test_single_node_successor_is_none_after_call():
    head, _ = build([42])
    reverse_linked_list(head)
    assert head.successor is None
    assert head.value == 42


def test_values_are_not_modified():
    head, nodes = build([1, 2, 3, 4])
    reverse_linked_list(head)
    assert [n.value for n in nodes] == [1, 2, 3, 4]


def test_result_is_acyclic():
    head, _ = build(list(range(50)))
    result = reverse_linked_list(head)
    to_list(result)  # raises on a cycle


# --- Documented behaviour (fails due to the bug in solution.py) ------------

@pytest.mark.xfail(strict=True, reason=BUG)
def test_single_node_returns_same_node():
    head, _ = build([42])
    assert reverse_linked_list(head) is head


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "values",
    [[1, 2], [1, 2, 3], [5, 4, 3, 2, 1], list(range(100)), ["a", "b", "a"]],
)
def test_reverses_list(values):
    head, _ = build(values)
    assert to_list(reverse_linked_list(head)) == list(reversed(values))


@pytest.mark.xfail(strict=True, reason=BUG)
def test_new_head_is_original_tail():
    head, nodes = build([1, 2, 3, 4, 5])
    assert reverse_linked_list(head) is nodes[-1]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_reverses_in_place_reusing_nodes():
    head, nodes = build([1, 2, 3])
    reverse_linked_list(head)
    assert nodes[2].successor is nodes[1]
    assert nodes[1].successor is nodes[0]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_double_reverse_restores_order():
    values = [1, 2, 3, 4]
    head, _ = build(values)
    assert to_list(reverse_linked_list(reverse_linked_list(head))) == values
