"""Contract tests for linked-list reversal.

Nonempty reversal is currently broken: the loop never updates prevnode.
Strict xfails document this defect and require attention once it is fixed.
"""

import pytest

from node import Node
from solution import reverse_linked_list


def make_list(values):
    nodes = [Node(value=value) for value in values]
    for current, successor in zip(nodes, nodes[1:]):
        current.successor = successor
    return nodes


def test_empty_list_returns_none():
    assert reverse_linked_list(None) is None


@pytest.mark.parametrize("values", [[1], [1, 2], [1, 2, 3, 4], [None, 0, 0, "last"]])
def test_original_head_becomes_tail_and_values_are_preserved(values):
    nodes = make_list(values)

    reverse_linked_list(nodes[0])

    assert nodes[0].successor is None
    assert [node.value for node in nodes] == values


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="reverse_linked_list never updates prevnode, so it returns None",
)
@pytest.mark.parametrize("values", [[1], [1, 2], [1, 2, 3, 4]])
def test_returns_original_tail_as_new_head(values):
    nodes = make_list(values)

    assert reverse_linked_list(nodes[0]) is nodes[-1]


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Missing prevnode update clears successor pointers instead of reversing them",
)
@pytest.mark.parametrize("values", [[1, 2], [1, 2, 3, 4], [None, 0, 0, "last"]])
def test_reverses_links_in_place(values):
    nodes = make_list(values)

    reverse_linked_list(nodes[0])

    for index in range(len(nodes) - 1, 0, -1):
        assert nodes[index].successor is nodes[index - 1]
    assert nodes[0].successor is None
