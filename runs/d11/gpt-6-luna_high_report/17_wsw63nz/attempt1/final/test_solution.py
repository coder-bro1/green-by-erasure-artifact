import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (4, 2),
        (6, 3),
        (15, 5),
        (21, 7),
        (49, 7),
    ],
)
def test_largest_divisor_for_composite_numbers(number, expected):
    assert largest_divisor(number) == expected


@pytest.mark.parametrize(
    ("number", "expected"),
    [(2, 1), (7, 1), (13, 1)],
)
def test_largest_divisor_for_prime_numbers(number, expected):
    assert largest_divisor(number) == expected
