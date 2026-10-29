import pytest

from node import Node
from solution import depth_first_search


def make_graph(edges, size):
    """Build independent nodes, including any isolated vertices."""
    nodes = [Node(value=index, successors=[]) for index in range(size)]
    for source, target in edges:
        nodes[source].successors.append(nodes[target])
    return nodes


@pytest.mark.parametrize(
    "edges, size, start, goal, expected",
    [
        ([], 1, 0, 0, True),
        ([], 2, 0, 1, False),
        ([(0, 1)], 2, 0, 1, True),
        ([(0, 1)], 2, 1, 0, False),
        ([(0, 1), (1, 2), (2, 3)], 4, 0, 3, True),
        ([(0, 1), (1, 2)], 4, 0, 3, False),
        ([(0, 1), (0, 2), (2, 3)], 4, 0, 3, True),
        ([(0, 1), (0, 2), (1, 3), (2, 3)], 4, 0, 3, True),
        ([(0, 1), (0, 2), (1, 3), (2, 3)], 5, 0, 4, False),
        ([(0, 0)], 1, 0, 0, True),
        ([(0, 1), (1, 0)], 2, 0, 1, True),
    ],
    ids=[
        "start-is-goal",
        "isolated-goal",
        "direct-edge",
        "edges-are-directed",
        "multi-hop-path",
        "disconnected-goal",
        "goal-in-later-branch",
        "shared-descendant-reachable",
        "shared-descendant-unreachable",
        "self-loop-start-is-goal",
        "cycle-goal-before-revisit",
    ],
)
def test_reachability(edges, size, start, goal, expected):
    nodes = make_graph(edges, size)

    assert depth_first_search(nodes[start], nodes[goal]) is expected


def test_equal_values_do_not_make_distinct_nodes_reachable():
    start = Node(value="same", successors=[])
    goal = Node(value="same", successors=[])

    assert depth_first_search(start, goal) is False


def test_search_preserves_graph_and_has_no_state_between_calls():
    nodes = make_graph([(0, 1), (1, 2)], 4)
    original_successors = [list(node.successors) for node in nodes]

    assert depth_first_search(nodes[0], nodes[2]) is True
    assert depth_first_search(nodes[0], nodes[3]) is False
    assert depth_first_search(nodes[0], nodes[2]) is True
    assert [node.successors for node in nodes] == original_successors


@pytest.mark.xfail(
    strict=True,
    reason="Visited nodes are never recorded; cycles cause RecursionError instead of a reachability boolean.",
    raises=RecursionError,
)
@pytest.mark.parametrize(
    "edges, size, goal, expected",
    [
        ([(0, 0)], 2, 1, False),
        ([(0, 1), (1, 0)], 3, 2, False),
        ([(0, 1), (1, 0), (0, 2)], 3, 2, True),
    ],
    ids=[
        "unreachable-goal-with-self-loop",
        "unreachable-goal-with-two-node-cycle",
        "reachable-goal-after-cyclic-branch",
    ],
)
def test_reachability_when_search_must_traverse_a_cycle(edges, size, goal, expected):
    nodes = make_graph(edges, size)

    assert depth_first_search(nodes[0], nodes[goal]) is expected
