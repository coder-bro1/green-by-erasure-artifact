"""Tests for shortest paths, including documented directed-graph defects."""

import heapq
import math
import random

import pytest

from solution import shortest_path_lengths


def undirected_edges(edges):
    return {
        pair: weight
        for (source, target), weight in edges.items()
        for pair in ((source, target), (target, source))
    }


@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (0, {}, []),
        (1, {}, [[0]]),
        (2, {}, [[0, math.inf], [math.inf, 0]]),
        (2, {(0, 1): 3}, [[0, 3], [3, 0]]),
        (
            3,
            {(0, 1): 2, (1, 2): 3, (0, 2): 9},
            [[0, 2, 5], [2, 0, 3], [5, 3, 0]],
        ),
        (
            3,
            {(0, 1): 4},
            [[0, 4, math.inf], [4, 0, math.inf], [math.inf, math.inf, 0]],
        ),
        (
            3,
            {(0, 1): 0, (1, 2): 0.5, (0, 2): 2.5},
            [[0, 0, 0.5], [0, 0, 0.5], [0.5, 0.5, 0]],
        ),
    ],
    ids=["empty", "one-node", "no-edges", "one-edge", "shortcut", "isolated", "fractional-and-zero"],
)
def test_known_undirected_distances(n, edges, expected):
    result = shortest_path_lengths(n, undirected_edges(edges))

    assert dict(result) == {
        (source, target): expected[source][target]
        for source in range(n)
        for target in range(n)
    }


def dijkstra_distances(n, edges):
    """Independent reference for graphs with nonnegative weights."""
    neighbors = [[] for _ in range(n)]
    for (source, target), weight in edges.items():
        neighbors[source].append((target, weight))

    result = {}
    for source in range(n):
        distances = [math.inf] * n
        distances[source] = 0
        pending = [(0, source)]
        while pending:
            distance, node = heapq.heappop(pending)
            if distance != distances[node]:
                continue
            for target, weight in neighbors[node]:
                candidate = distance + weight
                if candidate < distances[target]:
                    distances[target] = candidate
                    heapq.heappush(pending, (candidate, target))
        result.update({(source, target): distance for target, distance in enumerate(distances)})
    return result


@pytest.mark.parametrize("seed", range(10))
def test_undirected_graph_matches_independent_dijkstra(seed):
    rng = random.Random(seed)
    n = 7
    edges = undirected_edges(
        {
            (source, target): rng.randint(0, 20)
            for source in range(n)
            for target in range(source + 1, n)
            if rng.random() < 0.4
        }
    )

    assert dict(shortest_path_lengths(n, edges)) == dijkstra_distances(n, edges)


def test_input_mapping_is_not_modified():
    edges = undirected_edges({(0, 1): 2, (1, 2): 4, (0, 2): 10})
    original = edges.copy()

    shortest_path_lengths(3, edges)

    assert edges == original


def test_calls_return_independent_results():
    first = shortest_path_lengths(2, undirected_edges({(0, 1): 2}))
    second = shortest_path_lengths(2, {})

    first[0, 1] = 99

    assert second[0, 1] == math.inf
    assert first is not second


@pytest.mark.xfail(
    strict=True,
    reason="The recurrence uses distance[j, k] instead of distance[k, j].",
)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (2, {(0, 1): 3}, {(0, 0): 0, (0, 1): 3, (1, 0): math.inf, (1, 1): 0}),
        (
            3,
            {(0, 1): 2, (1, 2): 3},
            {
                (0, 0): 0, (0, 1): 2, (0, 2): 5,
                (1, 0): math.inf, (1, 1): 0, (1, 2): 3,
                (2, 0): math.inf, (2, 1): math.inf, (2, 2): 0,
            },
        ),
        (2, {(0, 1): -2}, {(0, 0): 0, (0, 1): -2, (1, 0): math.inf, (1, 1): 0}),
    ],
    ids=["direction-is-preserved", "directed-chain", "negative-edge-without-cycle"],
)
def test_directed_graph_contract(n, edges, expected):
    assert dict(shortest_path_lengths(n, edges)) == expected
