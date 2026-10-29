import pytest

from solution import circular_shift


def test_docstring_examples():
    assert circular_shift(12, 1) == "21"
    assert circular_shift(12, 2) == "12"


def test_returns_string():
    assert isinstance(circular_shift(123, 1), str)


@pytest.mark.parametrize(
    "x, shift, expected",
    [
        (12345, 1, "51234"),
        (12345, 2, "45123"),
        (12345, 3, "34512"),
        (12345, 4, "23451"),
        (100, 1, "010"),
        (100, 2, "001"),
        (97, 1, "79"),
    ],
)
def test_right_rotation(x, shift, expected):
    assert circular_shift(x, shift) == expected


def test_shift_zero_returns_original():
    assert circular_shift(12345, 0) == "12345"


@pytest.mark.parametrize("x", [7, 12, 123, 98765])
def test_shift_equal_to_length_returns_original(x):
    assert circular_shift(x, len(str(x))) == str(x)


@pytest.mark.parametrize(
    "x, shift, expected",
    [
        (12, 3, "21"),
        (123, 4, "321"),
        (123, 100, "321"),
        (5, 2, "5"),
        (1200, 5, "0021"),
    ],
)
def test_shift_greater_than_length_reverses(x, shift, expected):
    assert circular_shift(x, shift) == expected


def test_single_digit():
    assert circular_shift(0, 1) == "0"
    assert circular_shift(9, 1) == "9"
