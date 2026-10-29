import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    ("value", "shift", "expected"),
    [
        (12, 1, "21"),
        (12, 2, "12"),
        (12345, 2, "45123"),
        (12345, 0, "12345"),
        (12345, 5, "12345"),
        (12345, 6, "54321"),
        (7, 1, "7"),
        (7, 2, "7"),
        (0, 0, "0"),
    ],
)
def test_circular_shift(value, shift, expected):
    assert circular_shift(value, shift) == expected
