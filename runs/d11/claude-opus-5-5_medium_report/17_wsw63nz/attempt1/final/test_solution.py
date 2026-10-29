import pytest

from solution import largest_divisor


def test_docstring_example():
    assert largest_divisor(15) == 5


@pytest.mark.parametrize("n, expected", [
    (2, 1),
    (3, 1),
    (4, 2),
    (6, 3),
    (7, 1),
    (10, 5),
    (49, 7),
    (97, 1),
    (100, 50),
    (1024, 512),
    (7919, 1),
    (3 * 7919, 7919),
])
def test_known_values(n, expected):
    assert largest_divisor(n) == expected


@pytest.mark.parametrize("n", range(2, 300))
def test_properties(n):
    d = largest_divisor(n)
    assert 1 <= d < n
    assert n % d == 0
    assert all(n % k != 0 for k in range(d + 1, n))


@pytest.mark.parametrize("n", range(2, 300))
def test_matches_n_over_smallest_prime_factor(n):
    p = next(k for k in range(2, n + 1) if n % k == 0)
    assert largest_divisor(n) == n // p
