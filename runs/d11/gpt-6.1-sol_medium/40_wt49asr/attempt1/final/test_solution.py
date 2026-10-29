import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (2, 1),  # Smallest integer with a positive proper divisor.
        (3, 1),
        (97, 1),  # Prime numbers have only 1 as a positive proper divisor.
        (4, 2),
        (16, 8),
        (100, 50),  # Even numbers have n / 2 as their largest proper divisor.
        (9, 3),
        (15, 5),  # Example from the docstring.
        (25, 5),
        (49, 7),
        (81, 27),
        (105, 35),
        (143, 13),
        (1001, 143),
    ],
)
def test_largest_divisor_known_values(n, expected):
    assert largest_divisor(n) == expected


@pytest.mark.parametrize("n", range(2, 201))
def test_largest_divisor_is_the_greatest_positive_proper_divisor(n):
    result = largest_divisor(n)

    assert isinstance(result, int)
    assert 1 <= result < n
    assert n % result == 0
    assert all(n % candidate != 0 for candidate in range(result + 1, n))
