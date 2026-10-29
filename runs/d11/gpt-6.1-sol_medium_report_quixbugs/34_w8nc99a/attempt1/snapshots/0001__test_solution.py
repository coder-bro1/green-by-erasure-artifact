import pytest

from solution import gcd


@pytest.mark.parametrize("a", [1, 7, 35, 10**100])
def test_gcd_with_zero_second_argument(a):
    """Every positive integer is its own greatest divisor with zero."""
    assert gcd(a, 0) == a


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (35, 21, 7),  # Docstring example.
        (21, 35, 7),  # The result is independent of argument order.
        (0, 9, 9),  # Zero as the first argument.
        (1, 1, 1),
        (12, 12, 12),  # Equal inputs.
        (24, 6, 6),  # One input divides the other.
        (6, 24, 6),
        (13, 17, 1),  # Coprime inputs.
        (8, 9, 1),  # Consecutive inputs.
        (48, 18, 6),  # Several Euclidean steps are required.
        (10**100, 10**50, 10**50),  # Arbitrarily large integers.
    ],
)
def test_gcd_with_positive_second_argument(a, b, expected):
    """Return the greatest common divisor for documented nonnegative inputs."""
    assert gcd(a, b) == expected
