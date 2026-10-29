import sys

import pytest

from node import Node
from solution import depth_first_search


def make_graph(edges, size):
    # Pass a fresh list because Node's default successors list is shared.
    nodes = [Node(value=index, successors=[]) for index in range(size)]
    for source, target in edges:
        nodes[source].successors.append(nodes[target])
    return nodes


@pytest.mark.parametrize(
    "edges,size,start,goal,expected",
    [
        ([], 1, 0, 0, True),
        ([], 2, 0, 1, False),
        ([(0, 1)], 2, 0, 1, True),
        ([(0, 1)], 2, 1, 0, False),
        ([(0, 1), (1, 2), (2, 3)], 4, 0, 3, True),
        ([(0, 1), (1, 2)], 4, 0, 3, False),
        ([(0, 1), (0, 2), (2, 3)], 4, 0, 3, True),
        ([(0, 0)], 2, 0, 1, False),
        ([(0, 1), (1, 2), (2, 0)], 4, 0, 3, False),
        ([(0, 1), (1, 0), (1, 2)], 3, 0, 2, True),
        ([(0, 1), (0, 2), (1, 3), (2, 3), (3, 0)], 5, 0, 4, False),
        ([(0, 1), (0, 1), (1, 2)], 3, 0, 2, True),
    ],
    ids=[
        "start-is-goal", "isolated-goal", "direct-edge", "directed-edge",
        "chain", "disconnected-goal", "later-branch", "self-loop",
        "cycle-without-goal", "cycle-with-exit", "shared-descendant",
        "duplicate-edges",
    ],
)
def test_reachability(edges, size, start, goal, expected):
    nodes = make_graph(edges, size)
    assert depth_first_search(nodes[start], nodes[goal]) is expected


def test_equal_values_do_not_make_distinct_nodes_reachable():
    start = Node(value="same", successors=[])
    goal = Node(value="same", successors=[])
    assert depth_first_search(start, goal) is False
    start.successors.append(goal)
    assert depth_first_search(start, goal) is True


def test_repeated_searches_have_independent_visited_state():
    nodes = make_graph([(0, 1), (1, 0), (1, 2)], 4)
    assert depth_first_search(nodes[0], nodes[3]) is False
    assert depth_first_search(nodes[0], nodes[2]) is True
    assert depth_first_search(nodes[0], nodes[2]) is True
    assert depth_first_search(nodes[2], nodes[0]) is False


def test_search_preserves_graph():
    nodes = make_graph([(0, 1), (0, 2), (1, 0), (2, 3)], 5)
    original_lists = [node.successors for node in nodes]
    original_edges = [list(node.successors) for node in nodes]
    original_values = [node.value for node in nodes]
    assert depth_first_search(nodes[0], nodes[3]) is True
    assert depth_first_search(nodes[0], nodes[4]) is False
    for node, original_list, original_edge_list, original_value in zip(
        nodes, original_lists, original_edges, original_values
    ):
        assert node.successors is original_list
        assert node.successors == original_edge_list
        assert node.value == original_value


@pytest.mark.xfail(
    strict=True,
    raises=RecursionError,
    reason=(
        "The docstring promises reachability, but recursive DFS exceeds Python's "
        "recursion limit on a long chain instead of returning True."
    ),
)
def test_reachable_goal_in_deep_graph():
    size = sys.getrecursionlimit() + 50
    nodes = make_graph([(index, index + 1) for index in range(size - 1)], size)
    assert depth_first_search(nodes[0], nodes[-1]) is True
