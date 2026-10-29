import pytest

from solution import circular_shift


# --- Behaviour that solution.py implements correctly -------------------------

def test_docstring_example_full_rotation():
    assert circular_shift(12, 2) == "12"


@pytest.mark.parametrize("x", [0, 7, 12, 123, 98765])
def test_zero_shift_returns_original(x):
    assert circular_shift(x, 0) == str(x)


@pytest.mark.parametrize("x", [1, 12, 123, 98765])
def test_shift_equal_to_length_returns_original(x):
    assert circular_shift(x, len(str(x))) == str(x)


@pytest.mark.parametrize(
    "x, shift, expected",
    [
        (12, 3, "21"),
        (123, 4, "321"),
        (12345, 100, "54321"),
        (7, 2, "7"),
        (100, 5, "001"),
    ],
)
def test_shift_greater_than_length_reverses(x, shift, expected):
    assert circular_shift(x, shift) == expected


def test_returns_string():
    assert isinstance(circular_shift(12, 1), str)
    assert isinstance(circular_shift(12, 5), str)


def test_single_digit_any_shift():
    for shift in range(0, 5):
        assert circular_shift(5, shift) == "5"


# --- Documented behaviour that solution.py gets WRONG -------------------------
# The else-branch returns s[:n-shift] + s[n-shift:], which is just s, so no
# rotation ever happens for 0 < shift < len(digits). A correct implementation
# would return s[n-shift:] + s[:n-shift]. These are strict xfails: if the bug
# is fixed, they will XPASS and fail the run, prompting removal of the marker.

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py bug: partial right-rotation returns input unchanged",
)


@BUG
def test_docstring_example_shift_one():
    assert circular_shift(12, 1) == "21"


@BUG
@pytest.mark.parametrize(
    "x, shift, expected",
    [
        (123, 1, "312"),
        (123, 2, "231"),
        (12345, 2, "45123"),
        (1000, 1, "0100"),
    ],
)
def test_partial_right_rotation(x, shift, expected):
    assert circular_shift(x, shift) == expected
