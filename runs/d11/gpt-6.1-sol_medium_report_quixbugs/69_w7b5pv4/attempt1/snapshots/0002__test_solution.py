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


@pytest.mark.parametrize("values", [(7,), (1, 2), (1, 2, 3, 4), (5, 5, 5)])
def test_returns_original_tail_as_new_head(values):
    nodes = make_list(values)

    result = reverse_linked_list(nodes[0])

    assert result is nodes[-1]


@pytest.mark.parametrize("values", [(1, 2), (1, 2, 3, 4), (5, 5, 5)])
def test_reverses_every_successor_pointer(values):
    nodes = make_list(values)

    reverse_linked_list(nodes[0])

    assert nodes[0].successor is None
    for index in range(1, len(nodes)):
        assert nodes[index].successor is nodes[index - 1]


def test_single_node_remains_terminated():
    node = Node(value="only node")

    reverse_linked_list(node)

    assert node.successor is None


def test_original_head_becomes_terminated_tail():
    nodes = make_list([1, 2, 3])

    reverse_linked_list(nodes[0])

    assert nodes[0].successor is None


def test_node_values_are_preserved():
    values = [object(), None, "text", 0]
    nodes = make_list(values)

    reverse_linked_list(nodes[0])

    for node, value in zip(nodes, values):
        assert node.value is value
