import pytest

from solution import circular_shift


@pytest.mark.parametrize(
    ("number", "shift", "expected"),
    [
        (12, 1, "21"),
        (12, 2, "12"),
        (12345, 1, "51234"),
        (12345, 2, "45123"),
        (12345, 4, "23451"),
        (12345, 0, "12345"),
        (12345, 5, "12345"),
        (12345, 6, "54321"),
        (12345, 10, "54321"),
        (12345, 10**6, "54321"),
        (1200, 1, "0120"),
        (1200, 2, "0012"),
        (1200, 5, "0021"),
        (1111, 2, "1111"),
        (7, 0, "7"),
        (7, 1, "7"),
        (7, 2, "7"),
        (0, 0, "0"),
        (0, 1, "0"),
        (0, 2, "0"),
    ],
)
def test_circular_shift(number, shift, expected):
    result = circular_shift(number, shift)

    assert isinstance(result, str)
    assert result == expected
