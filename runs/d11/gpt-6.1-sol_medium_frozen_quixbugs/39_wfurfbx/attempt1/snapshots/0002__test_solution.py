import pytest

from node import Node
from solution import depth_first_search


def make_nodes(count):
    # Pass fresh lists because Node's constructor uses mutable defaults.
    return [Node(value=index, successors=[]) for index in range(count)]


def reachable(start, goal):
    """Independent, iterative reachability oracle for the graph tests."""
    pending = [start]
    visited = set()
    while pending:
        node = pending.pop()
        if node is goal:
            return True
        if node not in visited:
            visited.add(node)
            pending.extend(node.successors)
    return False


@pytest.mark.parametrize(
    "edges",
    [
        [],
        [(0, 1)],
        [(0, 1), (1, 2), (2, 3), (3, 4)],
        [(0, 1), (0, 2), (0, 3), (0, 4)],
        [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)],
        [(0, 1), (2, 3), (3, 4)],
        [(0, 1), (0, 1), (1, 2), (0, 3), (3, 4)],
    ],
    ids=["isolated", "one-edge", "chain", "branches", "diamond", "disconnected", "duplicate-edge"],
)
def test_reachability_for_every_node_pair(edges):
    nodes = make_nodes(5)
    for source, target in edges:
        nodes[source].successors.append(nodes[target])

    for start in nodes:
        for goal in nodes:
            assert depth_first_search(start, goal) is reachable(start, goal)


def test_goal_comparison_uses_identity_not_value():
    start, reachable_goal, distinct_goal = make_nodes(3)
    reachable_goal.value = distinct_goal.value = "same value"
    start.successors.append(reachable_goal)

    assert depth_first_search(start, reachable_goal) is True
    assert depth_first_search(start, distinct_goal) is False


def test_search_continues_after_unsuccessful_branch():
    start, dead_end, branch, goal = make_nodes(4)
    start.successors.extend([dead_end, branch])
    branch.successors.append(goal)

    assert depth_first_search(start, goal) is True


def test_edges_are_directed():
    start, goal = make_nodes(2)
    start.successors.append(goal)

    assert depth_first_search(start, goal) is True
    assert depth_first_search(goal, start) is False


def test_start_is_goal_even_with_a_self_loop():
    (node,) = make_nodes(1)
    node.successors.append(node)

    assert depth_first_search(node, node) is True


def test_cycle_with_goal_before_revisiting_a_node():
    start, middle, goal = make_nodes(3)
    start.successors.append(middle)
    middle.successors.append(goal)
    goal.successors.append(start)

    assert depth_first_search(start, goal) is True


def test_successful_search_short_circuits_remaining_successors():
    start, goal = make_nodes(2)
    start.successors.extend([goal, start])

    assert depth_first_search(start, goal) is True


def test_repeated_searches_preserve_graph_and_have_independent_state():
    start, middle, goal, isolated = make_nodes(4)
    start.successors.append(middle)
    middle.successors.append(goal)
    nodes = [start, middle, goal, isolated]
    original_lists = [node.successors for node in nodes]
    original_contents = [list(node.successors) for node in nodes]

    for _ in range(2):
        assert depth_first_search(start, goal) is True
        assert depth_first_search(start, isolated) is False
        assert depth_first_search(middle, goal) is True
        assert depth_first_search(goal, start) is False

    for node, original_list, original_content in zip(
        nodes, original_lists, original_contents
    ):
        assert node.successors is original_list
        assert node.successors == original_content
