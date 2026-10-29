import pytest

from solution import sieve


def test_upper_bound_one_has_no_primes():
    assert sieve(1) == []


@pytest.mark.xfail(
    strict=True,
    reason="Docstring promises primes through max, but any() on the initially "
    "empty primes list is False, so sieve always returns [] for max >= 2.",
)
@pytest.mark.parametrize(
    ("upper_bound", "expected"),
    [
        (2, [2]),
        (3, [2, 3]),
        (4, [2, 3]),
        (10, [2, 3, 5, 7]),
        (25, [2, 3, 5, 7, 11, 13, 17, 19, 23]),
        (49, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]),
        (
            100,
            [
                2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
            ],
        ),
    ],
    ids=["first-prime", "inclusive-prime-bound", "composite-bound", "ten",
         "prime-square-25", "prime-square-49", "one-hundred"],
)
def test_returns_all_primes_through_inclusive_upper_bound(upper_bound, expected):
    assert sieve(upper_bound) == expected
