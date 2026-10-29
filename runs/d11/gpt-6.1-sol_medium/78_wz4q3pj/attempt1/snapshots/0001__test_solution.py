import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (2, 1),
        (3, 1),
        (7, 1),
        (97, 1),
        (4, 2),
        (9, 3),
        (25, 5),
        (49, 7),
        (6, 3),
        (12, 6),
        (15, 5),
        (21, 7),
        (100, 50),
    ],
)
def test_largest_divisor(n, expected):
    assert largest_divisor(n) == expected


@pytest.mark.parametrize("n", range(2, 101))
def test_result_is_largest_proper_divisor(n):
    result = largest_divisor(n)

    assert isinstance(result, int)
    assert 1 <= result < n
    assert n % result == 0
    assert all(n % candidate != 0 for candidate in range(result + 1, n))
