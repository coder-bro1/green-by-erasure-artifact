"""Tests for breadth-first search, including its current exhaustion behavior."""

import pytest

from node import Node
from solution import breadth_first_search


def make_graph(edges):
    """Build distinct nodes with independent successor lists."""
    labels = set(edges)
    labels.update(label for successors in edges.values() for label in successors)
    nodes = {label: Node(value=label, successors=[]) for label in labels}
    for label, successors in edges.items():
        nodes[label].successors = [nodes[successor] for successor in successors]
    return nodes


@pytest.mark.parametrize(
    "edges,start,goal",
    [
        ({"start": []}, "start", "start"),
        ({"start": ["goal"]}, "start", "goal"),
        ({"start": ["middle"], "middle": ["goal"]}, "start", "goal"),
        ({"start": ["dead_end", "branch"], "branch": ["goal"]}, "start", "goal"),
        (
            {"start": ["left", "right"], "left": ["shared"],
             "right": ["shared"], "shared": ["goal"]},
            "start", "goal",
        ),
        ({"start": ["start", "goal"]}, "start", "goal"),
        ({"start": ["middle"], "middle": ["start", "goal"]}, "start", "goal"),
        ({"start": ["middle", "middle"], "middle": ["goal"]}, "start", "goal"),
    ],
    ids=["same-node", "direct-edge", "chain", "branch", "diamond",
         "self-loop", "cycle", "duplicate-edges"],
)
def test_reachable_goal(edges, start, goal):
    nodes = make_graph(edges)

    assert breadth_first_search(nodes[start], nodes[goal]) is True


@pytest.mark.parametrize(
    "edges,start,goal",
    [
        ({"start": [], "goal": []}, "start", "goal"),
        ({"start": ["leaf"], "goal": []}, "start", "goal"),
        ({"start": ["start"], "goal": []}, "start", "goal"),
        ({"start": ["middle"], "middle": ["start"], "goal": []}, "start", "goal"),
        ({"start": ["goal"]}, "goal", "start"),
    ],
    ids=["isolated", "disconnected", "self-loop", "cycle", "reverse-edge"],
)
def test_unreachable_goal_currently_raises_index_error(edges, start, goal):
    # The queue is popped without an exhaustion check; preserve this behavior
    # while solution.py is intentionally left unchanged.
    nodes = make_graph(edges)

    with pytest.raises(IndexError):
        breadth_first_search(nodes[start], nodes[goal])


def test_goal_matching_uses_identity_even_with_equal_values():
    start = Node(value="same", successors=[])
    reachable = Node(value="same", successors=[])
    distinct_goal = Node(value="same", successors=[])
    start.successors.append(reachable)

    assert breadth_first_search(start, reachable) is True
    with pytest.raises(IndexError):
        breadth_first_search(start, distinct_goal)


def test_search_does_not_mutate_successor_lists_and_can_be_repeated():
    nodes = make_graph({"start": ["middle", "goal"], "middle": ["start", "goal"]})
    original_lists = {label: node.successors for label, node in nodes.items()}
    original_contents = {label: list(node.successors) for label, node in nodes.items()}

    for _ in range(2):
        assert breadth_first_search(nodes["start"], nodes["goal"]) is True

    for label, node in nodes.items():
        assert node.successors is original_lists[label]
        assert node.successors == original_contents[label]
