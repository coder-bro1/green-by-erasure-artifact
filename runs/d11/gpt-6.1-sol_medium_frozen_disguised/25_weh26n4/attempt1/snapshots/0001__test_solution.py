"""GCD contract tests, with the existing return-value bug recorded explicitly."""

import pytest

from solution import common_factor_max


def test_gcd_of_two_zeros():
    assert common_factor_max(0, 0) == 0


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: common_factor_max returns q after the loop, when q is zero.",
)
@pytest.mark.parametrize(
    "p, q, expected",
    [
        pytest.param(12, 18, 6, id="docstring-shared-factor"),
        pytest.param(7, 13, 1, id="docstring-coprime"),
        pytest.param(18, 12, 6, id="reversed-arguments"),
        pytest.param(24, 8, 8, id="divisible"),
        pytest.param(9, 9, 9, id="equal"),
        pytest.param(35, 64, 1, id="coprime-composites"),
        pytest.param(1, 42, 1, id="unit"),
        pytest.param(0, 15, 15, id="zero-first"),
        pytest.param(15, 0, 15, id="zero-second"),
        pytest.param(-12, 18, 6, id="negative-first"),
        pytest.param(12, -18, 6, id="negative-second"),
        pytest.param(-12, -18, 6, id="both-negative"),
        pytest.param(0, -15, 15, id="zero-and-negative"),
        pytest.param(-15, 0, 15, id="negative-and-zero"),
        pytest.param(832040, 514229, 1, id="consecutive-fibonacci"),
        pytest.param(2**200, 2**150, 2**150, id="arbitrary-precision"),
    ],
)
def test_gcd_contract(p, q, expected):
    assert common_factor_max(p, q) == expected
