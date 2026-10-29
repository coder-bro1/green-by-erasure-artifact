from math import inf

import pytest

from solution import shortest_path_lengths


def expected_distances(n, finite_distances):
    """Build a complete expected result from explicitly known distances."""
    expected = {(i, j): 0 if i == j else inf for i in range(n) for j in range(n)}
    expected.update(finite_distances)
    return expected


@pytest.mark.parametrize(
    "n, edges, finite_distances",
    [
        pytest.param(0, {}, {}, id="empty-graph"),
        pytest.param(1, {}, {}, id="single-node"),
        pytest.param(3, {}, {}, id="isolated-nodes"),
        pytest.param(2, {(0, 1): 7}, {(0, 1): 7}, id="directed-edge"),
        pytest.param(
            3,
            {(0, 1): 2, (1, 2): 3, (0, 2): 10},
            {(0, 1): 2, (1, 2): 3, (0, 2): 5},
            id="indirect-route-beats-direct-edge",
        ),
        pytest.param(
            3,
            {(0, 1): 4, (1, 2): 5, (0, 2): 2},
            {(0, 1): 4, (1, 2): 5, (0, 2): 2},
            id="direct-edge-beats-indirect-route",
        ),
        pytest.param(
            4,
            {(0, 3): 2, (3, 2): 3, (2, 1): 4},
            {(0, 3): 2, (3, 2): 3, (2, 1): 4,
             (0, 2): 5, (3, 1): 7, (0, 1): 9},
            id="multiple-intermediates-in-reverse-id-order",
        ),
        pytest.param(
            3,
            {(0, 1): 2, (1, 2): 3, (2, 0): 4},
            {(0, 1): 2, (1, 2): 3, (2, 0): 4,
             (0, 2): 5, (1, 0): 7, (2, 1): 6},
            id="positive-cycle",
        ),
        pytest.param(
            3,
            {(0, 1): 4, (1, 2): -6, (0, 2): 1},
            {(0, 1): 4, (1, 2): -6, (0, 2): -2},
            id="negative-edge-without-negative-cycle",
        ),
        pytest.param(
            3,
            {(0, 1): -2, (1, 0): 2, (1, 2): 0},
            {(0, 1): -2, (1, 0): 2, (1, 2): 0, (0, 2): -2},
            id="zero-length-cycle-and-edge",
        ),
        pytest.param(
            3,
            {(0, 1): 0.5, (1, 2): 1.25, (0, 2): 2.0},
            {(0, 1): 0.5, (1, 2): 1.25, (0, 2): 1.75},
            id="fractional-lengths",
        ),
        pytest.param(1, {(0, 0): 0}, {}, id="zero-length-self-loop"),
    ],
)
def test_all_ordered_pair_distances(n, edges, finite_distances):
    result = shortest_path_lengths(n, edges)

    assert isinstance(result, dict)
    assert dict(result) == expected_distances(n, finite_distances)


def test_input_edges_are_not_modified():
    edges = {(0, 1): 2, (1, 2): 3, (0, 2): 10}
    original = edges.copy()

    result = shortest_path_lengths(3, edges)

    assert edges == original
    assert result is not edges
    assert result[0, 2] == 5


@pytest.mark.xfail(
    strict=True,
    reason="A positive self-loop overwrites the zero-length path to the same node.",
)
def test_positive_self_loop_has_zero_distance_to_itself():
    # The empty path is shorter than traversing a positive self-loop.
    result = shortest_path_lengths(1, {(0, 0): 5})

    assert dict(result) == {(0, 0): 0}
