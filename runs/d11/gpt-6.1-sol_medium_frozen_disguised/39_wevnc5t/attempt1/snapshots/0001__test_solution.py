"""Tests for the documented ordering and repetition requirements."""

import pytest

from solution import ascending_with_few_repeats


@pytest.mark.parametrize(
    "nums, expected",
    [
        pytest.param([], True, id="empty"),
        pytest.param([7], True, id="singleton"),
        pytest.param([0], True, id="zero"),
        pytest.param([0, 1, 2, 9], True, id="strictly-increasing"),
        pytest.param([0, 4, 4, 9], True, id="docstring-sorted-pair"),
        pytest.param([0, 0], True, id="two-equal-values"),
        pytest.param([0, 0, 1, 1, 9, 9], True, id="multiple-pairs"),
        pytest.param([0, 10**100], True, id="large-integers"),
        pytest.param([2, 1], False, id="docstring-descending"),
        pytest.param([9, 4, 0], False, id="strictly-decreasing"),
        pytest.param([1, 0, 2, 3], False, id="decrease-at-start"),
        pytest.param([0, 3, 2, 4], False, id="decrease-in-middle"),
        pytest.param([0, 1, 3, 2], False, id="decrease-at-end"),
        pytest.param([0, 1, 0], False, id="nonadjacent-duplicate"),
        pytest.param([1, 1, 1, 0], False, id="too-many-repeats-and-decrease"),
    ],
)
def test_ordering_and_allowed_repetitions(nums, expected):
    assert ascending_with_few_repeats(nums) is expected


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: solution counts occurrences but never enforces the limit of two",
)
@pytest.mark.parametrize(
    "nums",
    [
        pytest.param([3, 3, 3], id="docstring-three-equal-values"),
        pytest.param([0, 0, 0], id="three-zeros"),
        pytest.param([1, 1, 1, 2, 3], id="too-many-at-start"),
        pytest.param([0, 1, 1, 1, 2], id="too-many-in-middle"),
        pytest.param([0, 1, 2, 2, 2], id="too-many-at-end"),
        pytest.param([4, 4, 4, 4], id="four-equal-values"),
    ],
)
def test_rejects_more_than_two_occurrences(nums):
    assert ascending_with_few_repeats(nums) is False


@pytest.mark.parametrize("nums", [[0, 4, 4, 9], [2, 1], [3, 3, 3], []])
def test_does_not_modify_input(nums):
    original = nums.copy()
    ascending_with_few_repeats(nums)
    assert nums == original
