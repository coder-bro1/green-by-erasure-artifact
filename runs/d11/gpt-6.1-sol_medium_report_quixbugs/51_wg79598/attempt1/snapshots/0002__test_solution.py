"""Tests for the documented linked-list cycle detection behavior."""

import pytest

from node import Node
from solution import detect_cycle


def make_list(length, cycle_entry=None):
    """Build a chain, optionally linking its tail to an earlier node."""
    nodes = [Node(value=index) for index in range(length)]
    for current, successor in zip(nodes, nodes[1:]):
        current.successor = successor
    if cycle_entry is not None:
        nodes[-1].successor = nodes[cycle_entry]
    return nodes


@pytest.mark.parametrize("length", [0, 1, 2, 3, 4, 5, 100, 1001])
def test_acyclic_list(length):
    nodes = make_list(length)

    assert detect_cycle(nodes[0] if nodes else None) is False


@pytest.mark.parametrize(
    ("length", "cycle_entry"),
    [
        (1, 0),  # A node pointing to itself.
        (2, 0),
        (3, 0),
        (4, 0),
        (3, 1),  # An acyclic prefix followed by a cycle.
        (4, 2),
        (5, 4),  # An acyclic prefix ending in a self-loop.
        (100, 1),
        (100, 50),
        (1001, 999),
    ],
)
def test_cyclic_list(length, cycle_entry):
    nodes = make_list(length, cycle_entry)

    assert detect_cycle(nodes[0]) is True


@pytest.mark.parametrize("cycle_entry", [None, 0, 2, 4])
def test_detection_preserves_nodes_and_links(cycle_entry):
    nodes = make_list(5, cycle_entry)
    original_links = [node.successor for node in nodes]
    original_values = [node.value for node in nodes]

    expected = cycle_entry is not None
    assert detect_cycle(nodes[0]) is expected
    assert detect_cycle(nodes[0]) is expected
    assert all(
        node.successor is successor
        for node, successor in zip(nodes, original_links)
    )
    assert [node.value for node in nodes] == original_values


def test_repeated_values_do_not_imply_a_cycle():
    nodes = make_list(5)
    for node in nodes:
        node.value = "same value"

    assert detect_cycle(nodes[0]) is False


class EqualNode:
    """Distinct nodes that compare equal, to exercise identity detection."""

    def __init__(self, successor=None):
        self.successor = successor

    def __eq__(self, other):
        return isinstance(other, EqualNode)


@pytest.mark.parametrize("cyclic", [False, True])
def test_cycle_detection_uses_node_identity(cyclic):
    nodes = [EqualNode() for _ in range(4)]
    for current, successor in zip(nodes, nodes[1:]):
        current.successor = successor
    if cyclic:
        nodes[-1].successor = nodes[1]

    assert detect_cycle(nodes[0]) is cyclic


def test_unreachable_cycle_does_not_affect_acyclic_list():
    nodes = make_list(3)
    unreachable_nodes = make_list(3, cycle_entry=0)

    assert detect_cycle(nodes[0]) is False
    assert detect_cycle(unreachable_nodes[0]) is True


def test_starting_inside_cycle():
    nodes = make_list(6, cycle_entry=2)

    assert detect_cycle(nodes[4]) is True
