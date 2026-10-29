"""Regression tests for the implementation's current signed-digit behavior.

The implementation differs from its docstring: positive integers have their
first digit negated, while negative integers have every digit counted positively.
These tests preserve that behavior without changing solution.py.
"""

import pytest

from solution import positive_digit_sums


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([0, 0, 0], 0, id="zeros"),
        pytest.param(list(range(1, 10)), 0, id="positive-single-digits"),
        pytest.param(list(range(-9, 0)), 9, id="negative-single-digits"),
        pytest.param([10, 20, 100, 9000], 0, id="positive-trailing-zeros"),
        pytest.param([-10, -20, -100, -9000], 4, id="negative-trailing-zeros"),
        pytest.param([11, 22, 33, 99, 101, 202], 0, id="zero-digit-total"),
        pytest.param([12, 24, 123, 109, 909], 4, id="positive-digit-totals"),
        pytest.param([21, 42, 900, 810], 0, id="negative-digit-totals"),
        pytest.param([-12, -45, -99, -123], 4, id="negative-multiple-digits"),
        pytest.param([-12, 3, 0], 1, id="first-docstring-input-current-result"),
        pytest.param([24, -8], 2, id="second-docstring-input-current-result"),
        pytest.param([12, 12, -1, -1, 11, 0], 4, id="duplicates-counted"),
        pytest.param([-45, 45, 54, -54, 0, 11, 12], 4, id="mixed-signs"),
        pytest.param(
            [10**100, -(10**100), 10**100 + 2, 9 * 10**100 + 1],
            2,
            id="large-integers",
        ),
    ],
)
def test_positive_digit_sums_current_behavior(values, expected):
    assert positive_digit_sums(values) == expected


def test_accepts_tuple():
    assert positive_digit_sums((0, 12, -3, 11, 90)) == 2


def test_accepts_one_shot_generator():
    values = (value for value in [0, 12, -3, 11, 90])

    assert positive_digit_sums(values) == 2
    assert list(values) == []


def test_does_not_modify_input_list():
    values = [0, 12, -3, 11, 90]
    original = values.copy()

    assert positive_digit_sums(values) == 2
    assert values == original
    assert positive_digit_sums(values) == 2
