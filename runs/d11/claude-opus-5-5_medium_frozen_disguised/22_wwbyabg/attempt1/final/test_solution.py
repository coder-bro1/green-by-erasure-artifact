import pytest

from solution import rotate_digits

ROTATION_BUG = (
    "solution.py bug: the else branch concatenates digits[:n-steps] + digits[n-steps:], "
    "which reassembles the original string instead of rotating it"
)


# --- Behaviour that currently works ---------------------------------------

def test_returns_string():
    assert isinstance(rotate_digits(123, 1), str)


def test_steps_larger_than_digit_count_reverses_docstring_example():
    assert rotate_digits(89, 3) == "98"


@pytest.mark.parametrize(
    "num, steps, expected",
    [
        (12345, 6, "54321"),
        (7, 2, "7"),
        (100, 10, "001"),
        (0, 5, "0"),
    ],
)
def test_steps_larger_than_digit_count_reverses(num, steps, expected):
    assert rotate_digits(num, steps) == expected


@pytest.mark.parametrize("num", [1, 42, 4567, 1000])
def test_zero_steps_is_identity(num):
    assert rotate_digits(num, 0) == str(num)


@pytest.mark.parametrize("num", [5, 42, 4567, 12345])
def test_steps_equal_to_digit_count_is_full_rotation(num):
    # Rotating by len(digits) brings every digit back to its place.
    assert rotate_digits(num, len(str(num))) == str(num)


def test_single_digit_one_step():
    assert rotate_digits(9, 1) == "9"


def test_repeated_digits_unchanged_by_rotation():
    assert rotate_digits(1111, 2) == "1111"


# --- Documented rotation behaviour that the implementation gets wrong ------

@pytest.mark.xfail(reason=ROTATION_BUG, strict=True)
def test_docstring_example_rotate_by_one():
    assert rotate_digits(4567, 1) == "7456"


@pytest.mark.xfail(reason=ROTATION_BUG, strict=True)
@pytest.mark.parametrize(
    "num, steps, expected",
    [
        (12345, 2, "45123"),
        (12345, 4, "23451"),
        (12, 1, "21"),
        (1020, 1, "0102"),
    ],
)
def test_partial_right_rotation(num, steps, expected):
    assert rotate_digits(num, steps) == expected
