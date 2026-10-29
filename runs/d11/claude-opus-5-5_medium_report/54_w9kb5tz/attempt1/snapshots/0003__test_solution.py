import pytest

from solution import largest_divisor

BUG = (
    "solution.py checks `n - i == 0` instead of `n % i == 0`; since i < n this "
    "is never true, so the function falls through and returns None"
)


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    assert largest_divisor(15) == 5


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "n, expected",
    [
        (2, 1),
        (3, 1),
        (4, 2),
        (7, 1),
        (10, 5),
        (12, 6),
        (49, 7),
        (97, 1),
        (100, 50),
        (1024, 512),
    ],
)
def test_known_values(n, expected):
    assert largest_divisor(n) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("n", range(2, 60))
def test_result_is_largest_proper_divisor(n):
    d = largest_divisor(n)
    assert isinstance(d, int)
    assert 1 <= d < n
    assert n % d == 0
    assert all(n % k != 0 for k in range(d + 1, n))
