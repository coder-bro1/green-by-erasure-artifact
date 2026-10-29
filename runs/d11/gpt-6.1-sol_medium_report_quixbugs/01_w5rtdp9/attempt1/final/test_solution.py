"""Tests for the documented directed-graph reachability contract."""

from itertools import product

import pytest

from node import Node
from solution import breadth_first_search


def make_graph(size, edges):
    # Supply separate lists to avoid Node's shared mutable defaults.
    nodes = [Node(value=index, successors=[]) for index in range(size)]
    for source, target in edges:
        nodes[source].successors.append(nodes[target])
    return nodes


@pytest.mark.parametrize(
    "size, edges, start, goal, expected",
    [
        pytest.param(1, [], 0, 0, True, id="isolated-node-reaches-itself"),
        pytest.param(2, [], 0, 1, False, id="disconnected-nodes"),
        pytest.param(2, [(0, 1)], 0, 1, True, id="direct-edge"),
        pytest.param(2, [(0, 1)], 1, 0, False, id="edges-are-directed"),
        pytest.param(4, [(0, 1), (1, 2), (2, 3)], 0, 3, True, id="multi-hop-path"),
        pytest.param(4, [(0, 1), (2, 3)], 0, 3, False, id="separate-components"),
        pytest.param(4, [(0, 1), (0, 2), (2, 3)], 0, 3, True, id="branch-after-dead-end"),
        pytest.param(4, [(0, 1), (0, 2), (1, 3), (2, 3)], 0, 3, True, id="converging-paths"),
        pytest.param(2, [(0, 0)], 0, 1, False, id="self-loop-with-unreachable-goal"),
        pytest.param(2, [(0, 0), (0, 1)], 0, 1, True, id="self-loop-with-exit"),
        pytest.param(4, [(0, 1), (1, 2), (2, 0)], 0, 3, False, id="cycle-with-unreachable-goal"),
        pytest.param(4, [(0, 1), (1, 2), (2, 0), (2, 3)], 0, 3, True, id="cycle-with-exit"),
        pytest.param(3, [(0, 1), (0, 1), (1, 2)], 0, 2, True, id="duplicate-edges"),
    ],
)
def test_reachability(size, edges, start, goal, expected):
    nodes = make_graph(size, edges)

    assert breadth_first_search(nodes[start], nodes[goal]) is expected


def test_distinct_nodes_with_equal_values_are_not_the_same_goal():
    start, reachable, unreachable = [Node(value="same", successors=[]) for _ in range(3)]
    start.successors.append(reachable)

    assert breadth_first_search(start, reachable) is True
    assert breadth_first_search(start, unreachable) is False


def test_repeated_searches_preserve_graph():
    nodes = make_graph(4, [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3)])
    original_successors = [list(node.successors) for node in nodes]

    for _ in range(2):
        assert breadth_first_search(nodes[0], nodes[3]) is True
        assert breadth_first_search(nodes[3], nodes[0]) is False
        assert [node.successors for node in nodes] == original_successors


def test_every_three_node_directed_graph():
    """Compare all 512 graphs and all endpoint pairs with an independent DFS."""
    possible_edges = list(product(range(3), repeat=2))
    for mask in range(1 << len(possible_edges)):
        edges = [edge for bit, edge in enumerate(possible_edges) if mask & (1 << bit)]
        nodes = make_graph(3, edges)
        for start in range(3):
            reachable = set()
            pending = [start]
            while pending:
                current = pending.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                pending.extend(target for source, target in edges if source == current)

            for goal in range(3):
                assert breadth_first_search(nodes[start], nodes[goal]) is (goal in reachable), (
                    f"edges={edges}, start={start}, goal={goal}"
                )
