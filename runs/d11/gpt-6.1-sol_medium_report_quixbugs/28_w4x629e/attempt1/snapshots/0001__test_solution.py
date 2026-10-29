"""Tests for the documented positive-k contract of subsequences."""

from itertools import combinations

import pytest

from solution import subsequences


@pytest.mark.parametrize(
    "a,b,k,expected",
    [
        (1, 5, 3, [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]),
        (2, 5, 1, [[2], [3], [4]]),
        (-3, 0, 2, [[-3, -2], [-3, -1], [-2, -1]]),
        (-1, 2, 2, [[-1, 0], [-1, 1], [0, 1]]),
        (3, 6, 3, [[3, 4, 5]]),
        (4, 5, 1, [[4]]),
        (1, 3, 3, []),
        (2, 2, 1, []),
        (5, 2, 2, []),
    ],
    ids=[
        "docstring-example",
        "singletons-exclude-upper-bound",
        "negative-range",
        "range-spanning-zero",
        "entire-range",
        "one-element-range",
        "length-exceeds-range",
        "empty-range",
        "reversed-range",
    ],
)
def test_documented_cases(a, b, k, expected):
    result = subsequences(a, b, k)
    assert isinstance(result, list)
    assert all(isinstance(sequence, list) for sequence in result)
    # The contract specifies all ascending sequences, but no outer list order.
    assert sorted(result) == expected


@pytest.mark.parametrize("a", range(-3, 4))
@pytest.mark.parametrize("b", range(-3, 4))
@pytest.mark.parametrize("k", range(1, 6))
def test_matches_all_combinations_for_small_ranges(a, b, k):
    expected = [list(sequence) for sequence in combinations(range(a, b), k)]
    result = subsequences(a=a, b=b, k=k)

    assert isinstance(result, list)
    assert all(isinstance(sequence, list) for sequence in result)
    assert sorted(result) == expected
