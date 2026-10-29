"""Tests for the documented contract of ``solution.kheapsort``."""

import inspect

import pytest

from solution import kheapsort


@pytest.mark.parametrize(
    "arr, k, expected",
    [
        ([3, 2, 1, 5, 4], 2, [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], 4, [1, 2, 3, 4, 5]),
    ],
    ids=["docstring-almost-sorted", "docstring-reversed"],
)
def test_docstring_examples_with_positive_k(arr, k, expected):
    assert list(kheapsort(arr, k)) == expected


@pytest.mark.parametrize(
    "arr",
    [[], [7], [1, 2, 3, 4, 5], [-9, -2, 0, 4, 20]],
    ids=["empty", "singleton", "docstring-sorted", "mixed-signs"],
)
def test_zero_displacement(arr):
    assert list(kheapsort(arr, 0)) == arr


@pytest.mark.parametrize("k", [0, 1, 5])
def test_empty_input(k):
    assert list(kheapsort([], k)) == []


@pytest.mark.parametrize(
    "arr, k, expected",
    [
        ([7], 1, [7]),
        ([1, 2, 3, 4], 1, [1, 2, 3, 4]),
        ([2, 1, 4, 3], 1, [1, 2, 3, 4]),
        ([-2, -9, 4, 0], 1, [-9, -2, 0, 4]),
        ([0, -3, -1, 8, 5], 2, [-3, -1, 0, 5, 8]),
        ([3, 1, 2], 3, [1, 2, 3]),
        ([3, 1, 2], 8, [1, 2, 3]),
    ],
    ids=[
        "singleton",
        "already-sorted",
        "adjacent-swaps",
        "negative-and-zero",
        "two-place-displacement",
        "k-equals-length",
        "k-exceeds-length",
    ],
)
def test_positive_displacement(arr, k, expected):
    # Each case satisfies both documented preconditions.
    assert len(set(arr)) == len(arr)
    positions = {value: index for index, value in enumerate(expected)}
    assert all(abs(index - positions[value]) <= k for index, value in enumerate(arr))
    assert list(kheapsort(arr, k)) == expected


@pytest.mark.parametrize("arr, k", [([], 0), ([1, 2, 3], 0), ([2, 1, 3], 1)])
def test_returns_a_generator(arr, k):
    result = kheapsort(arr, k)
    assert inspect.isgenerator(result)
    assert iter(result) is result


@pytest.mark.parametrize("arr, k", [([], 2), ([1, 2, 3], 0), ([3, 2, 1], 2)])
def test_iteration_leaves_input_unchanged(arr, k):
    original = arr.copy()
    result = kheapsort(arr, k)
    assert arr == original
    list(result)
    assert arr == original
