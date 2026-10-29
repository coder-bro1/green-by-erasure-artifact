"""Tests for kheapsort's documented contract, including known regressions."""

from collections.abc import Generator

import pytest

from solution import kheapsort


@pytest.mark.parametrize("k", [0, 1, 2, 10])
def test_empty_input(k):
    assert list(kheapsort([], k)) == []


@pytest.mark.parametrize(
    "values",
    [[], [0], [-7], [1, 2, 3, 4, 5], [-10, -3, 0, 4, 100]],
)
def test_sorted_input_with_zero_displacement(values):
    result = list(kheapsort(values, 0))
    assert result == values


def test_returns_a_generator():
    result = kheapsort([1, 2, 3], 0)
    assert isinstance(result, Generator)
    assert iter(result) is result
    assert next(result) == 1
    assert list(result) == [2, 3]
    with pytest.raises(StopIteration):
        next(result)


@pytest.mark.parametrize(
    "values, k",
    [([], 2), ([1, 2, 3], 0), ([3, 2, 1, 5, 4], 2), ([5, 4, 3, 2, 1], 4)],
)
def test_does_not_mutate_input(values, k):
    original = values.copy()
    result = kheapsort(values, k)
    assert values == original
    list(result)
    assert values == original


@pytest.mark.xfail(
    strict=True,
    reason="The initial arr[:k] heap entries are processed again and duplicated.",
)
@pytest.mark.parametrize(
    "values, k",
    [
        ([3, 2, 1, 5, 4], 2),  # First documented example.
        ([5, 4, 3, 2, 1], 4),  # Second documented example.
        ([2, 1, 4, 3, 5], 1),  # Adjacent swaps.
        ([-2, -5, 0, 8, 3], 1),  # Negative and positive integers.
        ([1, 2, 3], 2),  # Already sorted, with a nonzero bound.
        ([42], 1),  # Singleton.
        ([3, 1, 2], 10),  # Bound larger than the input length.
    ],
)
def test_sorts_each_input_element_exactly_once(values, k):
    assert list(kheapsort(values, k)) == sorted(values)
