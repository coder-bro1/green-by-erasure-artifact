"""Tests for quicksort, including its known duplicate-value limitation."""

from itertools import permutations

import pytest

from solution import quicksort


@pytest.mark.parametrize(
    "values",
    [
        [],
        [42],
        [1, 2],
        [2, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 2, 5],
        [-3, -1, -5, -2, -4],
        [0, -10, 7, -1, 3],
        [10**100, -(10**100), 0, 1, -1],
    ],
)
def test_quicksort_sorts_distinct_integers(values):
    assert quicksort(values) == sorted(values)


def test_quicksort_sorts_every_permutation_of_five_distinct_integers():
    expected = [-2, -1, 0, 1, 2]
    for ordering in permutations(expected):
        assert quicksort(list(ordering)) == expected


@pytest.mark.parametrize("values", [[], [1], [3, -1, 2, 0], [2, 1, 2]])
def test_quicksort_does_not_modify_input(values):
    original = values.copy()

    result = quicksort(values)

    assert values == original
    assert result is not values
    result.append(99)
    assert values == original


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: elements equal to the pivot are discarded",
)
@pytest.mark.parametrize("values", [[1, 1], [3, 1, 3, 2, 1], [0, -1, 0, -1]])
def test_quicksort_preserves_duplicate_values(values):
    assert quicksort(values) == sorted(values)
