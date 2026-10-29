import pytest

from solution import greatest_common_divisor

BUG = "solution.py returns b (always 0 after the loop) instead of a, so the GCD is never returned"


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_coprime():
    assert greatest_common_divisor(3, 5) == 1


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_common_factor():
    assert greatest_common_divisor(25, 15) == 5


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (12, 18, 6),
        (18, 12, 6),
        (7, 7, 7),
        (1, 99, 1),
        (100, 10, 10),
        (17, 13, 1),
        (2**10 * 3, 2**6 * 5, 2**6),
    ],
)
def test_general_cases(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
def test_second_argument_zero():
    assert greatest_common_divisor(5, 0) == 5


@pytest.mark.xfail(strict=True, reason=BUG)
def test_first_argument_zero():
    assert greatest_common_divisor(0, 5) == 5


def test_both_zero():
    # gcd(0, 0) is 0 by convention
    assert greatest_common_divisor(0, 0) == 0


def test_returns_int():
    assert isinstance(greatest_common_divisor(25, 15), int)
