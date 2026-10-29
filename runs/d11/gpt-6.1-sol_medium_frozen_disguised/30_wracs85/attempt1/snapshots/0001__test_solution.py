"""Tests for sum_odd_squares, including its known even-number bug."""

import pytest

from solution import sum_odd_squares


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([1], 1, id="one"),
        pytest.param([1, 3, 5, 7], 84, id="positive-odd-integers"),
        pytest.param([-5, 7], 49, id="negative-and-positive"),
        pytest.param([-1, -3, -5], 0, id="negative-odd-integers"),
        pytest.param([-2, -4, 0], 0, id="nonpositive-even-integers"),
        pytest.param([0, 1, 0], 1, id="zero-is-ignored"),
        pytest.param([3, 1.5], 9, id="fraction-is-ignored"),
        pytest.param([1.0, 3.0, 5.0], 0, id="integer-valued-floats-are-ignored"),
        pytest.param([-1.5, 0.0, 2.5, 3.5], 0, id="only-floats"),
        pytest.param([3, 3, 3], 27, id="duplicates-count-separately"),
        pytest.param([10**50 + 1], (10**50 + 1) ** 2, id="large-integer"),
    ],
)
def test_sum_odd_squares(nums, expected):
    assert sum_odd_squares(nums) == expected


def test_input_list_is_not_modified():
    nums = [-5, 0, 1, 1.5, 3, 3]
    original = nums.copy()

    assert sum_odd_squares(nums) == 19
    assert nums == original


@pytest.mark.xfail(
    strict=True,
    reason="The implementation does not exclude positive even integers.",
)
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        pytest.param([2, 4, 6], 0, id="only-positive-even-integers"),
        pytest.param([1, 2, 3, 4, 5], 35, id="mixed-parity"),
        pytest.param([3, 4, 1.5], 9, id="docstring-example"),
    ],
)
def test_positive_even_integers_are_ignored(nums, expected):
    assert sum_odd_squares(nums) == expected
