"""Tests for the documented prefix-maximum behavior of rolling_max."""

import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], [], id="empty"),
        pytest.param([7], [7], id="single-positive"),
        pytest.param([-7], [-7], id="single-negative"),
        pytest.param([0], [0], id="single-zero"),
        pytest.param([4, 4, 4], [4, 4, 4], id="equal-values"),
        pytest.param([5, 4, 3, 2], [5, 5, 5, 5], id="decreasing"),
        pytest.param([1, 9, 2, 9], [1, 9, 9, 9], id="maximum-at-second-position"),
        pytest.param([10**100, -(10**100), 0], [10**100] * 3, id="large-integers"),
    ],
)
def test_rolling_max(numbers, expected):
    assert rolling_max(numbers) == expected


@pytest.mark.xfail(
    strict=True,
    reason="rolling_max uses max(numbers) after the first element, including future values instead of only the prefix",
)
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param(
            [1, 2, 3, 2, 3, 4, 2],
            [1, 2, 3, 3, 3, 4, 4],
            id="docstring-example",
        ),
        pytest.param([1, 2, 3, 4], [1, 2, 3, 4], id="increasing"),
        pytest.param([-5, -3, -4, -1], [-5, -3, -3, -1], id="negative-values"),
        pytest.param([-2, 0, -1, 3], [-2, 0, 0, 3], id="mixed-signs"),
        pytest.param([2, 1, 2, 5], [2, 2, 2, 5], id="maximum-at-end"),
        pytest.param([0, 0, 1, 0], [0, 0, 1, 1], id="zeros-before-maximum"),
    ],
)
def test_rolling_max_only_uses_values_seen_so_far(numbers, expected):
    assert rolling_max(numbers) == expected


def test_rolling_max_does_not_modify_input():
    numbers = [3, 1, 4, 2]
    original = numbers.copy()

    rolling_max(numbers)

    assert numbers == original


def test_rolling_max_returns_a_new_list():
    numbers = [3, 2, 1]

    result = rolling_max(numbers)

    assert result is not numbers
    result.append(99)
    assert numbers == [3, 2, 1]
