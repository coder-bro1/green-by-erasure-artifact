import pytest

from node import Node
from solution import reverse_linked_list


def make_list(values):
    nodes = [Node(value) for value in values]
    for current, following in zip(nodes, nodes[1:]):
        current.successor = following
    return nodes


def assert_chain(head, expected_nodes):
    """Check node identity, every successor, and the terminating pointer."""
    current = head
    for expected in expected_nodes:
        assert current is expected
        current = current.successor
    assert current is None


@pytest.mark.parametrize(
    "values",
    [
        pytest.param([], id="empty"),
        pytest.param([42], id="singleton"),
        pytest.param([1, 2], id="two-nodes"),
        pytest.param([1, 2, 3, 4, 5], id="several-nodes"),
        pytest.param([7, 7, 7], id="duplicate-values"),
        pytest.param([None, 0, False, "", {"key": "value"}], id="mixed-values"),
        pytest.param(list(range(1500)), id="long-list"),
    ],
)
def test_reverse_returns_original_nodes_in_reverse_order(values):
    nodes = make_list(values)
    original_values = [node.value for node in nodes]

    head = reverse_linked_list(nodes[0] if nodes else None)

    assert_chain(head, nodes[::-1])
    # Reversal changes links, preserving each node's original value object.
    for node, original_value in zip(nodes, original_values):
        assert node.value is original_value


@pytest.mark.parametrize("values", [[], [1], [1, 2, 3, 4]])
def test_reversing_twice_restores_original_links(values):
    nodes = make_list(values)
    original_head = nodes[0] if nodes else None
    original_successors = [node.successor for node in nodes]

    reversed_head = reverse_linked_list(original_head)
    assert_chain(reversed_head, nodes[::-1])
    restored_head = reverse_linked_list(reversed_head)

    assert restored_head is original_head
    assert_chain(restored_head, nodes)
    for node, original_successor in zip(nodes, original_successors):
        assert node.successor is original_successor
