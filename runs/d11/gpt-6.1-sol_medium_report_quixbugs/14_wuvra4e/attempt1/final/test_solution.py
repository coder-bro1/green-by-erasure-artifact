"""Tests for the linked-list cycle detection contract in solution.py."""

import pytest

from node import Node
from solution import detect_cycle


def make_list(length):
    """Build distinct nodes with equal values, linked in order."""
    nodes = [Node(value="same value") for _ in range(length)]
    for current, successor in zip(nodes, nodes[1:]):
        current.successor = successor
    return nodes


@pytest.mark.xfail(
    strict=True,
    raises=AttributeError,
    reason="An empty list should return False, but hare.successor dereferences None.",
)
def test_empty_list_is_not_cyclic():
    assert detect_cycle(None) is False


@pytest.mark.parametrize("length", [1, 3, 5, 7, 9])
def test_odd_length_acyclic_list(length):
    nodes = make_list(length)

    assert detect_cycle(nodes[0]) is False


@pytest.mark.parametrize("length", [2, 4, 6, 8, 10])
@pytest.mark.xfail(
    strict=True,
    raises=AttributeError,
    reason=(
        "Even-length acyclic lists should return False, but the hare reaches None "
        "and the next iteration dereferences hare.successor."
    ),
)
def test_even_length_acyclic_list(length):
    nodes = make_list(length)

    assert detect_cycle(nodes[0]) is False


@pytest.mark.parametrize("tail_length", [0, 1, 2, 5])
@pytest.mark.parametrize("cycle_length", [1, 2, 3, 6])
def test_cycle_with_or_without_acyclic_prefix(tail_length, cycle_length):
    nodes = make_list(tail_length + cycle_length)
    nodes[-1].successor = nodes[tail_length]

    assert detect_cycle(nodes[0]) is True


@pytest.mark.parametrize("cyclic", [False, True])
def test_detection_preserves_node_values_and_links(cyclic):
    nodes = make_list(5)
    if cyclic:
        nodes[-1].successor = nodes[1]
    original_values = [node.value for node in nodes]
    original_links = [node.successor for node in nodes]

    assert detect_cycle(nodes[0]) is cyclic
    assert [node.value for node in nodes] == original_values
    assert all(
        node.successor is original_link
        for node, original_link in zip(nodes, original_links)
    )
