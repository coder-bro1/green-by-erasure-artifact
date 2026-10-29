import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, 0),  # no positive proper divisor
        (2, 1),  # smallest prime
        (13, 1),  # prime
        (4, 2),  # square of a prime
        (15, 5),  # example from the docstring
        (24, 12),
        (49, 7),
        (100, 50),
    ],
)
def test_largest_divisor(number: int, expected: int) -> None:
    assert largest_divisor(number) == expected
