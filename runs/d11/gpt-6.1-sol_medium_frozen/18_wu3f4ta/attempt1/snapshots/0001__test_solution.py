"""GCD contract tests, including strict expected failures for the known bug."""

import pytest

from solution import greatest_common_divisor


KNOWN_RETURN_BUG = pytest.mark.xfail(
    strict=True,
    reason="The implementation returns b, which is always zero after the loop.",
)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        pytest.param(0, 0, 0, id="both-zero"),
        pytest.param(3, 5, 1, marks=KNOWN_RETURN_BUG, id="docstring-coprime"),
        pytest.param(25, 15, 5, marks=KNOWN_RETURN_BUG, id="docstring-common-factor"),
        pytest.param(15, 25, 5, marks=KNOWN_RETURN_BUG, id="reversed-arguments"),
        pytest.param(12, 12, 12, marks=KNOWN_RETURN_BUG, id="equal-inputs"),
        pytest.param(24, 6, 6, marks=KNOWN_RETURN_BUG, id="exact-divisor"),
        pytest.param(48, 18, 6, marks=KNOWN_RETURN_BUG, id="multiple-iterations"),
        pytest.param(1, 999, 1, marks=KNOWN_RETURN_BUG, id="unit-input"),
        pytest.param(0, 7, 7, marks=KNOWN_RETURN_BUG, id="first-zero"),
        pytest.param(7, 0, 7, marks=KNOWN_RETURN_BUG, id="second-zero"),
        pytest.param(-48, 18, 6, marks=KNOWN_RETURN_BUG, id="first-negative"),
        pytest.param(48, -18, 6, marks=KNOWN_RETURN_BUG, id="second-negative"),
        pytest.param(-48, -18, 6, marks=KNOWN_RETURN_BUG, id="both-negative"),
        pytest.param(0, -7, 7, marks=KNOWN_RETURN_BUG, id="zero-and-negative"),
        pytest.param(-7, 0, 7, marks=KNOWN_RETURN_BUG, id="negative-and-zero"),
        pytest.param(
            12 * 10**100,
            18 * 10**100,
            6 * 10**100,
            marks=KNOWN_RETURN_BUG,
            id="arbitrary-precision-integers",
        ),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected
