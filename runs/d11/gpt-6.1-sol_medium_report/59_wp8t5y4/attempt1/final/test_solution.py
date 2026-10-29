"""Tests for the behavior documented by solution.circular_shift."""

import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    "x, shift, expected",
    [
        (12, 0, "12"),
        (12345, 0, "12345"),
        (12, 2, "12"),
        (12345, 5, "12345"),
        (0, 0, "0"),
        (0, 1, "0"),
        (7, 1, "7"),
        (1111, 2, "1111"),
        (1212, 2, "1212"),
        (12, 3, "21"),
        (12345, 6, "54321"),
        (12345, 100, "54321"),
        (1200, 5, "0021"),
        (0, 2, "0"),
        (7, 100, "7"),
        (12345678901234567890, 21, "09876543210987654321"),
    ],
)
def test_circular_shift_boundary_and_reversal_cases(x, shift, expected):
    result = circular_shift(x, shift)
    assert isinstance(result, str)
    assert result == expected


@pytest.mark.parametrize(
    "x, shift, expected",
    [
        (12, 1, "21"),  # The first example in the docstring.
        (12345, 1, "51234"),
        (12345, 2, "45123"),
        (12345, 4, "23451"),
        (1200, 1, "0120"),
        (1200, 2, "0012"),
        (101, 1, "110"),
        (12345678901234567890, 1, "01234567890123456789"),
    ],
)
@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason=(
        "Docstring requires a right rotation, but solution.py concatenates "
        "the slices in their original order and returns the unchanged digits."
    ),
)
def test_circular_shift_rotates_digits_right(x, shift, expected):
    assert circular_shift(x, shift) == expected
