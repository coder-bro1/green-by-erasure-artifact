import pytest

from node import Node
from solution import breadth_first_search


def make_graph(edges, start, goal):
    """Build distinct nodes with independent successor lists."""
    labels = {start, goal}
    for source, target in edges:
        labels.update((source, target))
    nodes = {label: Node(value=label, successors=[]) for label in labels}
    for source, target in edges:
        nodes[source].successors.append(nodes[target])
    return nodes[start], nodes[goal]


@pytest.mark.parametrize(
    "edges, start, goal",
    [
        ([], "start", "start"),
        ([("start", "goal")], "start", "goal"),
        ([("start", "middle"), ("middle", "goal")], "start", "goal"),
        ([("start", "dead_end"), ("start", "goal")], "start", "goal"),
        (
            [("start", "left"), ("start", "right"),
             ("left", "shared"), ("right", "shared"), ("shared", "goal")],
            "start", "goal",
        ),
        (
            [("start", "middle"), ("middle", "start"), ("middle", "goal")],
            "start", "goal",
        ),
        ([("start", "start"), ("start", "goal")], "start", "goal"),
        ([("start", "middle"), ("start", "middle"), ("middle", "goal")],
         "start", "goal"),
    ],
    ids=["same-node", "direct-edge", "chain", "branch-with-dead-end",
         "converging-paths", "cycle-with-exit", "self-loop", "duplicate-edges"],
)
def test_reachable_goal(edges, start, goal):
    startnode, goalnode = make_graph(edges, start, goal)

    assert breadth_first_search(startnode, goalnode) is True


@pytest.mark.parametrize(
    "edges, start, goal",
    [
        ([], "start", "goal"),
        ([("start", "middle"), ("middle", "end")], "start", "goal"),
        ([("goal", "start")], "start", "goal"),
        ([("start", "middle"), ("middle", "start")], "start", "goal"),
        ([("start", "start")], "start", "goal"),
    ],
    ids=["isolated-nodes", "disconnected-goal", "reverse-edge",
         "closed-cycle", "self-loop"],
)
@pytest.mark.xfail(
    strict=True,
    raises=IndexError,
    reason="Unreachable goals should return False, but the loop pops an empty deque.",
)
def test_unreachable_goal(edges, start, goal):
    startnode, goalnode = make_graph(edges, start, goal)

    assert breadth_first_search(startnode, goalnode) is False


@pytest.mark.xfail(
    strict=True,
    raises=IndexError,
    reason="Unreachable goals should return False, but the loop pops an empty deque.",
)
def test_distinct_nodes_with_equal_values_are_not_the_same_goal():
    startnode = Node(value="same", successors=[])
    reachable = Node(value="same", successors=[])
    goalnode = Node(value="same", successors=[])
    startnode.successors.append(reachable)

    assert breadth_first_search(startnode, goalnode) is False


def test_search_does_not_modify_graph():
    startnode, goalnode = make_graph(
        [("start", "middle"), ("middle", "goal")], "start", "goal"
    )
    middle = startnode.successors[0]
    nodes = [startnode, middle, goalnode]
    original_successors = [list(node.successors) for node in nodes]

    assert breadth_first_search(startnode, goalnode) is True
    assert [node.successors for node in nodes] == original_successors
    assert breadth_first_search(startnode, goalnode) is True
