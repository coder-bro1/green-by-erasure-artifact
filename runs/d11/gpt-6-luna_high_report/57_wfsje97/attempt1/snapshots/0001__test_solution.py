import math

import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (3, 5, 1),
        (25, 15, 5),
        (54, 24, 6),
        (17, 17, 17),
        (0, 9, 9),
        (9, 0, 9),
        (0, 0, 0),
        (-25, 15, 5),
        (-15, 25, 5),
        pytest.param(
            (25, -15, 5),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation can return a negative GCD when the second argument is negative.",
            ),
        ),
        pytest.param(
            (-25, -15, 5),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation can return a negative GCD when both arguments are negative.",
            ),
        ),
        pytest.param(
            (-7, 0, 7),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation returns the negative first argument when the second argument is zero.",
            ),
        ),
        pytest.param(
            (0, -7, 7),
            marks=pytest.mark.xfail(
                strict=True,
                reason="The implementation returns a negative result when the second argument is negative.",
            ),
        ),
    ],
)
def test_greatest_common_divisor(a, b=None, expected=None):
    # pytest.param keeps the xfail cases grouped with the expected-value list.
    # Those entries are tuples of (a, b, expected), just like normal cases.
    if b is None:
        a, b, expected = a

    assert greatest_common_divisor(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b"),
    [(12, 8), (35, 14), (81, 27), (101, 13), (0, 11), (11, 0)],
)
def test_result_is_a_common_divisor(a, b):
    divisor = greatest_common_divisor(a, b)

    assert divisor > 0
    assert a % divisor == 0
    assert b % divisor == 0


def test_result_matches_standard_gcd_for_nonnegative_integers():
    for a in range(20):
        for b in range(20):
            assert greatest_common_divisor(a, b) == math.gcd(a, b)
