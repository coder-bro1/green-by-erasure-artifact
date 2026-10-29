"""Tests for the documented digit-rotation contract and its known defect."""

import pytest

from solution import rotate_digits


@pytest.mark.parametrize("num", [0, 7, 89, 4567, 1002])
def test_zero_steps_preserves_digits(num):
    assert rotate_digits(num, 0) == str(num)


@pytest.mark.parametrize("num", [0, 7, 89, 4567, 1002])
def test_full_rotation_preserves_digits(num):
    assert rotate_digits(num, len(str(num))) == str(num)


@pytest.mark.parametrize(
    ("num", "steps", "expected"),
    [
        (89, 3, "98"),
        (4567, 5, "7654"),
        (4567, 8, "7654"),
        (4567, 100, "7654"),
        (1200, 5, "0021"),
        (1000, 20, "0001"),
        (0, 2, "0"),
        (7, 2, "7"),
    ],
)
def test_steps_exceeding_length_reverse_digits(num, steps, expected):
    result = rotate_digits(num, steps)
    assert result == expected
    assert isinstance(result, str)


@pytest.mark.parametrize(
    ("num", "steps", "expected"),
    [(4567, 1, "7456"), (4567, 2, "6745"), (4567, 3, "5674"), (1002, 2, "0210")],
)
@pytest.mark.xfail(
    strict=True,
    reason="Known bug: partial rotations concatenate slices in their original order.",
)
def test_partial_rotation_moves_trailing_digits_to_front(num, steps, expected):
    assert rotate_digits(num, steps) == expected
