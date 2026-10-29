import heapq
import math

import pytest

from node import Node
from solution import get, insert_or_update, shortest_path_length


class OrderedNode(Node):
    """Give heap ties an ordering so graph tests isolate path calculation."""

    def __lt__(self, other):
        return self.value < other.value


def make_graph(edges, start, goal, node_class=OrderedNode):
    labels = {start, goal} | {label for source, target, _ in edges for label in (source, target)}
    nodes = {label: node_class(value=label, successors=[]) for label in labels}
    lengths = {}
    for source, target, length in edges:
        nodes[source].successors.append(nodes[target])
        lengths[nodes[source], nodes[target]] = length
    return lengths, nodes[start], nodes[goal]


@pytest.mark.parametrize(
    "edges,start,goal,expected",
    [
        ([], "s", "s", 0),
        ([], "s", "t", math.inf),
        ([("s", "t", 7)], "s", "t", 7),
        ([("s", "t", 7)], "t", "s", math.inf),
        ([("s", "a", 2), ("a", "t", 3)], "s", "t", 5),
        ([("s", "t", 2), ("s", "a", 3), ("a", "t", 4)], "s", "t", 2),
        ([("s", "t", 9), ("s", "a", 2), ("a", "t", 3)], "s", "t", 5),
        ([("s", "a", 1), ("a", "s", 1), ("a", "t", 2)], "s", "t", 3),
        ([("s", "s", 1), ("s", "t", 4)], "s", "t", 4),
        ([("s", "a", 1), ("a", "s", 1), ("x", "t", 2)], "s", "t", math.inf),
        ([("s", "a", 0.25), ("a", "t", 0.5), ("s", "t", 1.0)], "s", "t", 0.75),
        ([("s", "a", 1), ("s", "b", 1), ("a", "t", 2), ("b", "t", 2)], "s", "t", 3),
    ],
    ids=[
        "same-node", "empty-unreachable", "direct-edge", "directed-edge",
        "chain", "direct-is-shortest", "indirect-is-shortest", "cycle",
        "self-loop", "disconnected-components", "fractional-weights", "equal-paths",
    ],
)
def test_shortest_path_length(edges, start, goal, expected):
    lengths, source, target = make_graph(edges, start, goal)
    assert shortest_path_length(lengths, source, target) == expected


def test_shortest_path_with_repository_nodes():
    lengths, source, target = make_graph(
        [("s", "a", 2), ("a", "t", 3)], "s", "t", node_class=Node
    )
    assert shortest_path_length(lengths, source, target) == 5


def test_decreased_distance_is_processed_before_more_distant_goal():
    lengths, source, target = make_graph(
        [("s", "a", 1), ("s", "t", 5), ("s", "c", 10),
         ("a", "c", 1), ("c", "t", 1)],
        "s", "t",
    )
    assert shortest_path_length(lengths, source, target) == 3


def test_equal_distances_with_repository_nodes():
    lengths, source, target = make_graph(
        [("s", "a", 1), ("s", "b", 1), ("a", "t", 2), ("b", "t", 2)],
        "s", "t", node_class=Node,
    )
    assert shortest_path_length(lengths, source, target) == 3


@pytest.mark.parametrize(
    "heap,wanted,expected",
    [([], "a", 0), ([(3, "a")], "missing", 0),
     ([(2, "a"), (5, "b")], "b", 5), ([(0, "a")], "a", 0)],
    ids=["empty", "missing", "existing", "zero-distance"],
)
def test_get(heap, wanted, expected):
    before = heap.copy()
    assert get(heap, wanted) == expected
    assert heap == before


def test_insert_or_update_inserts_new_node():
    heap = [(3, "a"), (5, "b")]
    assert insert_or_update(heap, (1, "c")) is None
    assert [heapq.heappop(heap) for _ in range(3)] == [(1, "c"), (3, "a"), (5, "b")]


def test_insert_or_update_replaces_existing_node():
    heap = [(3, "a"), (5, "b")]
    assert insert_or_update(heap, (2, "a")) is None
    assert heap == [(2, "a"), (5, "b")]


def test_insert_or_update_empty_heap():
    heap = []
    assert insert_or_update(heap, (4, "a")) is None
    assert heap == [(4, "a")]
