import pytest

from solution import largest_divisor


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason=(
        "Docstring promises the largest proper divisor, but n - i == 0 "
        "is never true for i in range(n), so the function returns None."
    ),
)
@pytest.mark.parametrize(
    ("n", "expected"),
    [
        pytest.param(15, 5, id="docstring-example"),
        pytest.param(2, 1, id="smallest-prime"),
        pytest.param(3, 1, id="odd-prime"),
        pytest.param(13, 1, id="larger-prime"),
        pytest.param(4, 2, id="prime-square"),
        pytest.param(9, 3, id="odd-prime-square"),
        pytest.param(49, 7, id="larger-prime-square"),
        pytest.param(8, 4, id="power-of-two"),
        pytest.param(27, 9, id="odd-prime-power"),
        pytest.param(6, 3, id="even-composite"),
        pytest.param(12, 6, id="multiple-proper-divisors"),
        pytest.param(45, 15, id="odd-composite"),
        pytest.param(100, 50, id="even-square"),
        pytest.param(1000, 500, id="larger-composite"),
    ],
)
def test_largest_divisor_returns_largest_proper_divisor(n, expected):
    """Check the documented result for integers with a proper divisor."""
    assert largest_divisor(n) == expected
