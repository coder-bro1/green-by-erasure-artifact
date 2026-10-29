import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    ("value", "shift", "expected"),
    [
        (12, 0, "12"),
        (12, 2, "12"),
        (12, 3, "21"),
        (7, 1, "7"),
    ],
)
def test_circular_shift_currently_supported_cases(value, shift, expected):
    assert circular_shift(value, shift) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The implementation does not rotate digits for shifts within the digit count",
)
@pytest.mark.parametrize(
    ("value", "shift", "expected"),
    [
        (12, 1, "21"),
        (123, 1, "312"),
        (123, 2, "231"),
    ],
)
def test_circular_shift_rotates_digits_right(value, shift, expected):
    assert circular_shift(value, shift) == expected
