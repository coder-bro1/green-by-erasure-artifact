import pytest

from solution import circular_shift

BUG = (
    "solution.py's else-branch returns s[:n-shift] + s[n-shift:], which is just s; "
    "the two slices are never swapped, so no rotation happens"
)


# --- Behaviour that currently matches the docstring ---

def test_docstring_example_shift_equals_length():
    assert circular_shift(12, 2) == "12"


def test_shift_zero_returns_same_digits():
    assert circular_shift(12345, 0) == "12345"


def test_shift_equal_to_length_is_identity():
    assert circular_shift(12345, 5) == "12345"


def test_shift_greater_than_length_reverses():
    assert circular_shift(12345, 6) == "54321"


def test_shift_much_greater_than_length_reverses():
    assert circular_shift(97, 100) == "79"


def test_single_digit_shift_greater_reverses():
    assert circular_shift(7, 3) == "7"


def test_single_digit_shift_one():
    assert circular_shift(7, 1) == "7"


def test_returns_string():
    assert isinstance(circular_shift(123, 1), str)
    assert isinstance(circular_shift(123, 10), str)


# --- Real right rotation (currently broken) ---

@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example_shift_one():
    assert circular_shift(12, 1) == "21"


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "x, shift, expected",
    [
        (123, 1, "312"),
        (123, 2, "231"),
        (12345, 1, "51234"),
        (12345, 3, "34512"),
        (100, 1, "010"),
    ],
)
def test_right_rotation(x, shift, expected):
    assert circular_shift(x, shift) == expected
