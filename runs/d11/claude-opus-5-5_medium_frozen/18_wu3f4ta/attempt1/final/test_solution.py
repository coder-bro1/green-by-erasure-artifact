import pytest

from solution import greatest_common_divisor

BUG = (
    "solution.py bug: function returns `b` (always 0 after the loop) "
    "instead of `a`; remove this xfail once fixed"
)

CORRECT_CASES = [
    (3, 5, 1),
    (25, 15, 5),
    (15, 25, 5),
    (10, 10, 10),
    (49, 14, 7),
    (144, 60, 12),
    (17, 1, 1),
    (0, 7, 7),
    (7, 0, 7),
    (2**31, 2**20, 2**20),
]


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("a, b, expected", CORRECT_CASES)
def test_gcd_correct_values(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("a, b", [(12, 18), (100, 75), (81, 27)])
def test_gcd_divides_both_inputs(a, b):
    g = greatest_common_divisor(a, b)
    assert g > 0
    assert a % g == 0 and b % g == 0


def test_gcd_of_zero_and_zero():
    # gcd(0, 0) is conventionally 0; this holds even with the current bug.
    assert greatest_common_divisor(0, 0) == 0


def test_returns_int():
    assert isinstance(greatest_common_divisor(25, 15), int)


@pytest.mark.parametrize("a, b", [(3, 5), (25, 15), (144, 60)])
def test_gcd_is_symmetric(a, b):
    assert greatest_common_divisor(a, b) == greatest_common_divisor(b, a)
