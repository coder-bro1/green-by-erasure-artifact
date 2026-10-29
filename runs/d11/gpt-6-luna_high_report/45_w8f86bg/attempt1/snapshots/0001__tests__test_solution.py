import pytest

from solution import is_prime


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (6, False),
        (101, True),
        (11, True),
        (13441, True),
        (61, True),
        (4, False),
        (1, False),
    ],
)
def test_docstring_examples(number, expected):
    assert is_prime(number) is expected


@pytest.mark.parametrize("number", [-10, -1, 0, 1])
def test_numbers_below_two_are_not_prime(number):
    assert is_prime(number) is False


@pytest.mark.parametrize("number", [2, 3, 5, 13, 97])
def test_small_primes(number):
    assert is_prime(number) is True


@pytest.mark.parametrize("number", [4, 9, 25, 49, 121, 143, 221])
def test_composites_with_nontrivial_factors(number):
    assert is_prime(number) is False
