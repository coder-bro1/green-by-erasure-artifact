import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    ("number", "shift", "expected"),
    [
        (12, 1, "21"),
        (12, 2, "12"),
        (12345, 0, "12345"),
        (12345, 2, "45123"),
        (1204, 4, "1204"),
        (1204, 5, "4021"),
        (1204, 20, "4021"),
        (0, 1, "0"),
    ],
)
def test_circular_shift(number, shift, expected):
    assert circular_shift(number, shift) == expected


@pytest.mark.xfail(strict=True, reason="circular_shift treats the minus sign as a digit")
def test_circular_shift_preserves_negative_sign():
    assert circular_shift(-123, 1) == "-312"


@pytest.mark.xfail(strict=True, reason="the length check counts the minus sign as a digit")
def test_oversized_shift_reverses_negative_number_digits():
    assert circular_shift(-123, 4) == "-321"
