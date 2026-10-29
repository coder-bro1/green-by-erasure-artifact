"""Tests for the ascending-order and duplicate limits in is_sorted."""

from itertools import product

import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([5], True, id="single-element-example"),
        pytest.param([1, 2, 3, 4, 5], True, id="ascending-five-example"),
        pytest.param([1, 3, 2, 4, 5], False, id="inversion-five-example"),
        pytest.param([1, 2, 3, 4, 5, 6], True, id="ascending-six-example"),
        pytest.param([1, 2, 3, 4, 5, 6, 7], True, id="ascending-seven-example"),
        pytest.param([1, 3, 2, 4, 5, 6, 7], False, id="inversion-seven-example"),
        pytest.param([1, 2, 2, 3, 3, 4], True, id="allowed-duplicates-example"),
        pytest.param([1, 2, 2, 2, 3, 4], False, id="excess-duplicates-example"),
    ],
)
def test_docstring_examples(numbers, expected):
    assert is_sorted(numbers) is expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], True, id="empty"),
        pytest.param([0], True, id="single-zero"),
        pytest.param([0, 0], True, id="two-zeros"),
        pytest.param([0, 0, 0], False, id="three-zeros"),
        pytest.param([1, 1], True, id="two-equal"),
        pytest.param([1, 1, 1], False, id="three-equal"),
        pytest.param([1, 1, 1, 1], False, id="four-equal"),
        pytest.param([0, 0, 1, 1, 2, 2], True, id="every-value-appears-twice"),
        pytest.param([0, 0, 0, 1, 2], False, id="excess-duplicates-at-start"),
        pytest.param([0, 1, 2, 2, 2], False, id="excess-duplicates-at-end"),
        pytest.param([2, 1], False, id="descending-pair"),
        pytest.param([4, 3, 2, 1, 0], False, id="strictly-descending"),
        pytest.param([1, 0, 2, 3], False, id="inversion-at-start"),
        pytest.param([0, 1, 3, 2], False, id="inversion-at-end"),
        pytest.param([0, 2, 1, 2], False, id="nonadjacent-duplicates"),
        pytest.param([0, 10**30, 10**30], True, id="large-integers"),
    ],
)
def test_ordering_and_duplicate_boundaries(numbers, expected):
    assert is_sorted(numbers) is expected


def test_all_short_lists_against_documented_rules():
    # One duplicate means two occurrences, as the docstring examples show.
    for length in range(7):
        for values in product(range(3), repeat=length):
            numbers = list(values)
            expected = numbers == sorted(numbers) and all(
                numbers.count(value) <= 2 for value in set(numbers)
            )
            assert is_sorted(numbers) is expected, numbers
