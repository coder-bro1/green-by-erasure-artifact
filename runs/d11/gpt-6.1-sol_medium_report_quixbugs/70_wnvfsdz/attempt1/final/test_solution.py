"""Tests for the documented powerset contract."""

from itertools import combinations

import pytest

from solution import powerset


def test_docstring_example():
    assert powerset(["a", "b", "c"]) == [
        [],
        ["c"],
        ["b"],
        ["b", "c"],
        ["a"],
        ["a", "c"],
        ["a", "b"],
        ["a", "b", "c"],
    ]


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        ([], [[]]),
        (["a"], [[], ["a"]]),
        ([None], [[], [None]]),
        ([0, -1], [[], [-1], [0], [0, -1]]),
        (["a", 2], [[], [2], ["a"], ["a", 2]]),
        ([[1], [2]], [[], [[2]], [[1]], [[1], [2]]]),
    ],
    ids=["empty", "singleton", "none", "numbers", "mixed-types", "unhashable"],
)
def test_small_inputs(arr, expected):
    assert powerset(arr) == expected


@pytest.mark.parametrize("size", range(9))
def test_all_subsets_are_present_exactly_once(size):
    arr = list(range(size))
    result = powerset(arr)
    expected = {
        subset
        for length in range(size + 1)
        for subset in combinations(arr, length)
    }

    assert isinstance(result, list)
    assert all(isinstance(subset, list) for subset in result)
    assert len(result) == 2**size
    assert {tuple(subset) for subset in result} == expected
    assert [] in result
    assert arr in result
