import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    ("number", "shift", "expected"),
    [
        (12, 0, "12"),
        (12, 1, "21"),
        (12345, 2, "45123"),
        (12345, 4, "23451"),
        (12, 2, "12"),
        (12, 3, "21"),
        (7, 1, "7"),
        (0, 5, "0"),
    ],
)
def test_circular_shift(number, shift, expected):
    assert circular_shift(number, shift) == expected
