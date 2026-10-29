"""Tests for the documented behavior, including the known index-filtering bug."""

import pytest

from solution import even_values_at_odd_slots


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([2], 0, id="single-even-value-is-ignored"),
        pytest.param([3], 0, id="single-odd-value"),
        pytest.param([2, 6], 6, id="first-index-is-ignored"),
        pytest.param([2, 3], 0, id="odd-value-at-odd-index"),
        pytest.param([1, 6, 3, 8, 5], 14, id="multiple-odd-indexes"),
        pytest.param([1, 3, 5, 7, 9], 0, id="all-odd-values"),
        pytest.param([1, 0, 3, 0, 5], 0, id="zero-is-even"),
        pytest.param([-2, -6, -3, -8, -5], -14, id="negative-even-values"),
        pytest.param([1, -4, 3, 6, 5], 2, id="mixed-signs"),
        pytest.param([1, 6, 3, 8], 14, id="final-odd-index-is-included"),
        pytest.param([1, 2, 3, 2, 5, 2], 6, id="repeated-values"),
        pytest.param([1, 10**100, 3, -(10**100) + 2], 2, id="large-integers"),
    ],
)
def test_sum_of_even_values_at_odd_indexes(values, expected):
    assert even_values_at_odd_slots(values) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1, 6, 3, 8, 2], 14, id="docstring-example"),
        pytest.param([1, 3, 2], 0, id="even-value-only-at-even-index"),
        pytest.param([2, 4, 6, 8, 10, 12], 24, id="all-even-values"),
        pytest.param([1, -4, -6, -8], -12, id="negative-value-at-even-index"),
    ],
)
@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Known bug: range uses step 1, including even indexes from index 2.",
)
def test_even_indexes_are_excluded(values, expected):
    assert even_values_at_odd_slots(values) == expected


def test_input_is_not_modified():
    values = [1, 6, 3, 8, 5]
    original = values.copy()

    even_values_at_odd_slots(values)

    assert values == original
