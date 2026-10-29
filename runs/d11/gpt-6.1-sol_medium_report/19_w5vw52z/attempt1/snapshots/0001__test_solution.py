"""Tests for the ascending-order and duplicate rules in is_sorted's docstring."""

import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([5], True, id="example-singleton"),
        pytest.param([1, 2, 3, 4, 5], True, id="example-five-sorted"),
        pytest.param([1, 3, 2, 4, 5], False, id="example-five-unsorted"),
        pytest.param([1, 2, 3, 4, 5, 6], True, id="example-six-sorted"),
        pytest.param([1, 2, 3, 4, 5, 6, 7], True, id="example-seven-sorted"),
        pytest.param([1, 3, 2, 4, 5, 6, 7], False, id="example-seven-unsorted"),
        pytest.param([1, 2, 2, 3, 3, 4], True, id="example-pairs-allowed"),
        pytest.param([], True, id="empty"),
        pytest.param([0], True, id="zero-singleton"),
        pytest.param([0, 1], True, id="increasing-pair"),
        pytest.param([1, 0], False, id="decreasing-pair"),
        pytest.param([0, 0], True, id="equal-pair"),
        pytest.param([0, 0, 1, 1, 2, 2], True, id="every-value-twice"),
        pytest.param([0, 2, 100, 10**100], True, id="gaps-and-large-integers"),
        pytest.param([3, 2, 1, 0], False, id="descending"),
        pytest.param([2, 1, 3, 4], False, id="inversion-at-start"),
        pytest.param([0, 1, 3, 2], False, id="inversion-at-end"),
        pytest.param([0, 2, 1, 3], False, id="inversion-in-middle"),
        pytest.param([0, 1, 0], False, id="nonadjacent-duplicate-unsorted"),
        pytest.param([0, 0, 0, 2, 1], False, id="excess-duplicates-and-inversion"),
    ],
)
def test_is_sorted(numbers, expected):
    assert is_sorted(numbers) is expected


@pytest.mark.parametrize(
    "numbers",
    [
        pytest.param([1, 2, 2, 2, 3, 4], id="docstring-example"),
        pytest.param([0, 0, 0], id="three-zeros"),
        pytest.param([1, 1, 1, 2, 3], id="three-at-start"),
        pytest.param([0, 1, 2, 2, 2], id="three-at-end"),
        pytest.param([7, 7, 7, 7], id="four-equal-values"),
        pytest.param([0, 0, 0, 1, 1, 1], id="multiple-excess-duplicates"),
    ],
)
def test_rejects_more_than_two_occurrences(numbers):
    # The examples allow two occurrences, but require False for three or more.
    assert is_sorted(numbers) is False
