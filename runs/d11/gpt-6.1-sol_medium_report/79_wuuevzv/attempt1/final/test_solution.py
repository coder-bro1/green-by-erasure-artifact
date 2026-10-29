"""Tests for count_nums' documented signed-first-digit convention."""

import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([], 0, id="docstring-empty"),
        pytest.param([0, 0, 0], 0, id="zero-is-not-positive"),
        pytest.param([123], 1, id="positive-larger-remaining-sum"),
        pytest.param([-12], 1, id="negative-positive-signed-sum"),
        pytest.param([-123], 1, id="negative-docstring-digit-example"),
        pytest.param([-1009], 1, id="negative-internal-zeros-positive-sum"),
        pytest.param([12, 12, -12, -12, 0], 4, id="count-duplicate-elements"),
    ],
)
def test_count_nums_documented_behavior(arr, expected):
    assert count_nums(arr) == expected


@pytest.mark.xfail(
    strict=True,
    reason=(
        "solution.py reverses the documented first-digit sign: positive numbers "
        "get a negative first digit, and negative numbers get a positive one."
    ),
)
@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([-1, 11, -11], 1, id="docstring-mixed-signs"),
        pytest.param([1, 1, 2], 3, id="docstring-repeated-positives"),
        pytest.param([1], 1, id="positive-single-digit"),
        pytest.param([10], 1, id="positive-trailing-zero"),
        pytest.param([11], 1, id="positive-equal-first-and-remaining-sum"),
        pytest.param([9001], 1, id="positive-smaller-remaining-sum"),
        pytest.param([-1], 0, id="negative-single-digit"),
        pytest.param([-10], 0, id="negative-trailing-zero"),
        pytest.param([-11], 0, id="negative-zero-signed-sum"),
        pytest.param([-21], 0, id="negative-negative-signed-sum"),
        pytest.param([-909], 0, id="negative-internal-zero-balanced-sum"),
        pytest.param([-9001], 0, id="negative-internal-zeros-negative-sum"),
        pytest.param([0, 10, -10, 11, -11, -12, -21, 123, -123], 5, id="mixed-boundaries"),
        pytest.param([10**100], 1, id="arbitrary-precision-positive"),
        pytest.param([-(10**100)], 0, id="arbitrary-precision-negative"),
    ],
)
def test_count_nums_first_digit_sign(arr, expected):
    assert count_nums(arr) == expected


def test_count_nums_does_not_mutate_input():
    arr = [0, 123, -123, -21, 11]
    original = arr.copy()

    count_nums(arr)

    assert arr == original
