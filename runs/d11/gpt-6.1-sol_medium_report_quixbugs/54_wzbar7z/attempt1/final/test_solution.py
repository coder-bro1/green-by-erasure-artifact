import pytest

from solution import get_factors


def test_one_has_no_prime_factors():
    assert get_factors(1) == []


@pytest.mark.parametrize("n", [2, 3, 5, 13, 101])
@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires [n] for a prime, but get_factors returns [].",
    raises=AssertionError,
)
def test_prime_is_its_own_only_factor(n):
    assert get_factors(n) == [n]


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (4, [2, 2]),
        (6, [2, 3]),
        (8, [2, 2, 2]),
        (12, [2, 2, 3]),
        (27, [3, 3, 3]),
        (36, [2, 2, 3, 3]),
        (49, [7, 7]),
        (100, [2, 2, 5, 5]),
        (210, [2, 3, 5, 7]),
        (315, [3, 3, 5, 7]),
        (1024, [2] * 10),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason=(
        "Docstring requires all prime factors with repetition, but the prime "
        "base case returns [] and drops the final prime factor."
    ),
    raises=AssertionError,
)
def test_composite_factors_are_sorted_and_include_repetitions(n, expected):
    assert get_factors(n) == expected
