import pytest

from node import Node
from solution import topological_ordering


def make_graph(values, edges):
    """Build nodes with explicit lists (avoids Node's shared mutable defaults)."""
    nodes = {v: Node(v, None, [], [], [], []) for v in values}
    for src, dst in edges:
        nodes[src].outgoing_nodes.append(nodes[dst])
        nodes[dst].incoming_nodes.append(nodes[src])
    return [nodes[v] for v in values]


def assert_valid_topological_order(nodes, result):
    # Every input node appears exactly once.
    assert len(result) == len(nodes)
    assert set(map(id, result)) == set(map(id, nodes))
    # Each node precedes every node it has an edge to.
    position = {id(n): i for i, n in enumerate(result)}
    for n in nodes:
        for succ in n.outgoing_nodes:
            assert position[id(n)] < position[id(succ)], (
                f"{n.value} must come before {succ.value}"
            )


def values(result):
    return [n.value for n in result]


def test_empty_graph():
    assert topological_ordering([]) == []


def test_single_node():
    nodes = make_graph(["a"], [])
    assert values(topological_ordering(nodes)) == ["a"]


def test_isolated_nodes_all_returned():
    nodes = make_graph(["a", "b", "c"], [])
    result = topological_ordering(nodes)
    assert_valid_topological_order(nodes, result)


def test_simple_chain():
    nodes = make_graph(["a", "b", "c", "d"], [("a", "b"), ("b", "c"), ("c", "d")])
    assert values(topological_ordering(nodes)) == ["a", "b", "c", "d"]


def test_chain_given_in_reverse_input_order():
    nodes = make_graph(["d", "c", "b", "a"], [("a", "b"), ("b", "c"), ("c", "d")])
    assert values(topological_ordering(nodes)) == ["a", "b", "c", "d"]


def test_fan_out():
    nodes = make_graph(["a", "b", "c"], [("a", "b"), ("a", "c")])
    result = topological_ordering(nodes)
    assert_valid_topological_order(nodes, result)
    assert result[0].value == "a"


def test_fan_in():
    nodes = make_graph(["a", "b", "c"], [("a", "c"), ("b", "c")])
    result = topological_ordering(nodes)
    assert_valid_topological_order(nodes, result)
    assert result[-1].value == "c"


def test_diamond():
    nodes = make_graph(
        ["a", "b", "c", "d"],
        [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")],
    )
    result = topological_ordering(nodes)
    assert_valid_topological_order(nodes, result)
    assert result[0].value == "a"
    assert result[-1].value == "d"


def test_node_with_multiple_parents_and_children():
    # QuixBugs reference graph.
    nodes = make_graph(
        [5, 7, 3, 11, 8, 2, 9, 10],
        [(5, 11), (7, 11), (7, 8), (3, 8), (3, 10),
         (11, 2), (11, 9), (11, 10), (8, 9)],
    )
    result = topological_ordering(nodes)
    assert_valid_topological_order(nodes, result)


def test_disconnected_components():
    nodes = make_graph(
        ["a", "b", "x", "y", "z"],
        [("a", "b"), ("x", "y"), ("y", "z")],
    )
    result = topological_ordering(nodes)
    assert_valid_topological_order(nodes, result)


def test_long_path_plus_shortcut_edge():
    nodes = make_graph(
        ["a", "b", "c", "d"],
        [("a", "b"), ("b", "c"), ("c", "d"), ("a", "d")],
    )
    assert values(topological_ordering(nodes)) == ["a", "b", "c", "d"]


def test_does_not_mutate_input_list():
    nodes = make_graph(["b", "a"], [("a", "b")])
    snapshot = list(nodes)
    topological_ordering(nodes)
    assert nodes == snapshot
