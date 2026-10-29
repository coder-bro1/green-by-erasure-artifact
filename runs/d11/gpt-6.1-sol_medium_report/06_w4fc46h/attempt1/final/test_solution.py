"""Tests for the digit-shifting behavior documented by solution.py."""

import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    "number, shift, expected",
    [
        (12, 1, "21"),  # First docstring example.
        (12, 2, "12"),  # Second docstring example.
        (12345, 0, "12345"),
        (12345, 1, "51234"),
        (12345, 2, "45123"),
        (12345, 3, "34512"),
        (12345, 4, "23451"),
        (12345, 5, "12345"),
        (10020, 1, "01002"),
        (10020, 2, "20100"),
        (1000, 3, "0001"),
        (1111, 2, "1111"),
        (7, 0, "7"),
        (7, 1, "7"),
        (0, 0, "0"),
        (0, 1, "0"),
        (12345678901234567890, 3, "89012345678901234567"),
    ],
)
def test_circular_shift_rotates_digits_right(number, shift, expected):
    result = circular_shift(number, shift)

    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "number, shift, expected",
    [
        (12, 3, "21"),
        (12345, 6, "54321"),
        (12345, 10, "54321"),
        (12345, 10**6, "54321"),
        (1200, 5, "0021"),
        (7, 2, "7"),
        (0, 2, "0"),
    ],
)
def test_shift_exceeding_digit_count_reverses_digits(number, shift, expected):
    result = circular_shift(number, shift)

    assert isinstance(result, str)
    assert result == expected
