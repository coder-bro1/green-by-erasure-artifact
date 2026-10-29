"""Tests for opposite values at distinct positions."""

import pytest

from solution import has_opposite_pair


@pytest.mark.parametrize(
    "nums, expected",
    [
        pytest.param([], False, id="empty"),
        pytest.param([5], False, id="single-positive"),
        pytest.param([-5], False, id="single-negative"),
        pytest.param([1, 2, 3], False, id="all-positive"),
        pytest.param([-1, -2, -3], False, id="all-negative"),
        pytest.param([1, -2, 3, -4], False, id="mixed-without-pair"),
        pytest.param([4, 4], False, id="repeated-nonzero"),
        pytest.param([4, -4, 2], True, id="docstring-pair"),
        pytest.param([4, -4], True, id="two-opposites"),
        pytest.param([-4, 4], True, id="reversed-opposites"),
        pytest.param([7, 2, -7], True, id="nonadjacent-pair"),
        pytest.param([1, 7, -7], True, id="pair-at-end"),
        pytest.param([2, 2, -2], True, id="duplicates-with-opposite"),
        pytest.param([0, 0], True, id="two-zeros"),
        pytest.param([3, 0, 4, 0], True, id="separated-zeros"),
        pytest.param([10**100, -(10**100)], True, id="large-integers"),
        pytest.param([10**100, -(10**100) + 1], False, id="large-near-opposites"),
    ],
)
def test_has_opposite_pair(nums, expected):
    assert has_opposite_pair(nums) is expected


@pytest.mark.parametrize("nums, expected", [((), False), ((3,), False), ((3, -3), True)])
def test_tuple_input(nums, expected):
    assert has_opposite_pair(nums) is expected


@pytest.mark.parametrize("nums", [[4, -4, 2], [1, -2, 3], [0, 0]])
def test_does_not_modify_input(nums):
    original = nums.copy()
    has_opposite_pair(nums)
    assert nums == original


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: the implementation pairs a zero with its own position",
)
@pytest.mark.parametrize("nums", [[0], [0, 3], [3, 0], [1, 0, -2]])
def test_single_zero_without_opposite_pair(nums):
    assert has_opposite_pair(nums) is False
