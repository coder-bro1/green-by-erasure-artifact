"""Tests for circular_shift, including its known rotation defect."""

import pytest

from solution import circular_shift


@pytest.mark.parametrize("number", [0, 7, 12, 12345, 1000])
def test_zero_shift_preserves_digits(number):
    assert circular_shift(number, 0) == str(number)


@pytest.mark.parametrize("number", [0, 7, 12, 12345, 1000])
def test_shift_equal_to_digit_count_preserves_digits(number):
    assert circular_shift(number, len(str(number))) == str(number)


@pytest.mark.parametrize(
    ("number", "shift", "expected"),
    [
        (0, 1, "0"),
        (7, 2, "7"),
        (12, 3, "21"),
        (12345, 6, "54321"),
        (12345, 100, "54321"),
        (1200, 5, "0021"),
    ],
)
def test_shift_larger_than_digit_count_reverses_digits(number, shift, expected):
    assert circular_shift(number, shift) == expected


@pytest.mark.parametrize(
    ("number", "shift"), [(0, 0), (7, 1), (12, 1), (1200, 5)]
)
def test_result_is_a_string(number, shift):
    assert isinstance(circular_shift(number, shift), str)


@pytest.mark.parametrize(
    ("number", "shift", "expected"),
    [(1111, 1, "1111"), (1212, 2, "1212"), (999, 2, "999")],
)
def test_rotating_repeated_patterns_preserves_digits(number, shift, expected):
    assert circular_shift(number, shift) == expected


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="solution.py concatenates the original slices without rotating them",
)
@pytest.mark.parametrize(
    ("number", "shift", "expected"),
    [
        (12, 1, "21"),
        (12345, 1, "51234"),
        (12345, 2, "45123"),
        (12345, 4, "23451"),
        (1200, 2, "0012"),
    ],
)
def test_partial_shift_rotates_digits_right(number, shift, expected):
    assert circular_shift(number, shift) == expected
