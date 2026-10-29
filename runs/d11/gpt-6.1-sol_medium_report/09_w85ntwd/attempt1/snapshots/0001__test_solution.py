"""Tests for the documented contract of pairs_sum_to_zero."""

from itertools import combinations, product

import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    "numbers, expected",
    [
        pytest.param([1, 3, 5, 0], False, id="docstring-single-zero"),
        pytest.param([1, 3, -2, 1], False, id="docstring-unmatched-negative"),
        pytest.param([1, 2, 3, 7], False, id="docstring-positive-only"),
        pytest.param([2, 4, -5, 3, 5, 7], True, id="docstring-matching-pair"),
        pytest.param([1], False, id="docstring-singleton"),
        pytest.param([], False, id="empty"),
        pytest.param([0], False, id="cannot-reuse-single-zero"),
        pytest.param([-1], False, id="negative-singleton"),
        pytest.param([0, 0], True, id="two-distinct-zero-positions"),
        pytest.param([4, -4], True, id="positive-then-negative"),
        pytest.param([-4, 4], True, id="negative-then-positive"),
        pytest.param([-1, -2, -3], False, id="negative-only"),
        pytest.param([2, 2, -3, -3], False, id="duplicates-without-pair"),
        pytest.param([2, 2, -2], True, id="duplicates-with-pair"),
        pytest.param([0, 2, 3], False, id="zero-is-not-enough"),
        pytest.param([0, 2, 0], True, id="separated-zeros"),
        pytest.param([6, 1, 2, -6], True, id="first-and-last-pair"),
        pytest.param([8, 3, -3, 5], True, id="interior-pair"),
        pytest.param([8, 5, 3, -3], True, id="final-pair"),
        pytest.param([3, -3, 5, -5], True, id="multiple-pairs"),
        pytest.param([10**100, -(10**100)], True, id="large-integers"),
        pytest.param([10**100, -(10**100) + 1], False, id="large-near-miss"),
    ],
)
def test_documented_behavior(numbers, expected):
    assert pairs_sum_to_zero(numbers) is expected


def test_all_short_lists_against_distinct_pair_oracle():
    """Check every list of up to four elements over a small integer domain."""
    for length in range(5):
        for values in product(range(-2, 3), repeat=length):
            numbers = list(values)
            expected = any(a + b == 0 for a, b in combinations(numbers, 2))
            assert pairs_sum_to_zero(numbers) is expected, numbers
