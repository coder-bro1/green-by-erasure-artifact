"""Tests for cycle detection, including the implementation's current limits."""

import pytest

from node import Node
from solution import detect_cycle


def make_list(length, cycle_entry=None):
    # Equal values ensure cycle detection depends on node identity.
    nodes = [Node(value="same") for _ in range(length)]
    for current, successor in zip(nodes, nodes[1:]):
        current.successor = successor
    if cycle_entry is not None:
        nodes[-1].successor = nodes[cycle_entry]
    return nodes


@pytest.mark.parametrize("length", [1, 3, 5, 7, 11, 101])
def test_odd_length_acyclic_list_returns_false(length):
    nodes = make_list(length)

    assert detect_cycle(nodes[0]) is False


@pytest.mark.parametrize(
    "length, cycle_entry",
    [
        (1, 0),  # A single node pointing to itself.
        (2, 0),
        (3, 0),
        (4, 0),
        (2, 1),  # A tail leading to a self-loop.
        (5, 4),
        (5, 1),
        (6, 2),
        (10, 7),
        (101, 50),
    ],
)
def test_cycle_returns_true(length, cycle_entry):
    nodes = make_list(length, cycle_entry)

    assert detect_cycle(nodes[0]) is True


@pytest.mark.parametrize("cycle_entry", [None, 0, 2, 4])
def test_detection_preserves_values_and_successor_links(cycle_entry):
    nodes = make_list(5, cycle_entry)
    original_successors = [node.successor for node in nodes]

    assert detect_cycle(nodes[0]) is (cycle_entry is not None)

    assert all(
        node.successor is original
        for node, original in zip(nodes, original_successors)
    )
    assert all(node.value == "same" for node in nodes)


def test_empty_list_currently_raises_attribute_error():
    # The implementation accesses successor before checking for an empty head.
    with pytest.raises(AttributeError, match="successor"):
        detect_cycle(None)


@pytest.mark.parametrize("length", [2, 4, 6, 10, 100])
def test_even_length_acyclic_list_currently_raises_attribute_error(length):
    # After a two-node hop, hare can be None on the next loop iteration.
    nodes = make_list(length)

    with pytest.raises(AttributeError, match="successor"):
        detect_cycle(nodes[0])
