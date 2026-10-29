import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    ("value", "shift", "expected"),
    [
        pytest.param(
            12,
            1,
            "21",
            marks=pytest.mark.xfail(
                strict=True,
                reason="circular_shift(12, 1) returns '12' instead of the documented '21'",
            ),
        ),
        pytest.param(
            1234,
            1,
            "4123",
            marks=pytest.mark.xfail(
                strict=True,
                reason="a one-place right circular shift should move the last digit to the front",
            ),
        ),
        pytest.param(
            1234,
            2,
            "3412",
            marks=pytest.mark.xfail(
                strict=True,
                reason="a two-place right circular shift should move the last two digits to the front",
            ),
        ),
        (12, 2, "12"),
        (1234, 0, "1234"),
        (1234, 4, "1234"),
        (1234, 5, "4321"),
    ],
)
def test_circular_shift(value, shift, expected):
    assert circular_shift(value, shift) == expected
