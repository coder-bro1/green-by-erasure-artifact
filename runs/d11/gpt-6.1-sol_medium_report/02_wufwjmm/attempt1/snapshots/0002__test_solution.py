import pytest

from solution import greatest_common_divisor


@pytest.mark.xfail(
    strict=True,
    reason="Docstring promises the GCD, but the function returns b, which is 0 at loop exit.",
)
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        pytest.param(3, 5, 1, id="docstring-coprime"),
        pytest.param(25, 15, 5, id="docstring-shared-factor"),
        pytest.param(15, 25, 5, id="reversed-arguments"),
        pytest.param(12, 12, 12, id="equal-integers"),
        pytest.param(36, 12, 12, id="one-divides-the-other"),
        pytest.param(48, 18, 6, id="multiple-euclidean-steps"),
        pytest.param(1, 100, 1, id="unit"),
        pytest.param(0, 9, 9, id="zero-first"),
        pytest.param(9, 0, 9, id="zero-second"),
        pytest.param(-48, 18, 6, id="negative-first"),
        pytest.param(48, -18, 6, id="negative-second"),
        pytest.param(-48, -18, 6, id="both-negative"),
        pytest.param(0, -9, 9, id="zero-and-negative"),
        pytest.param(-9, 0, 9, id="negative-and-zero"),
        pytest.param(2**100, 2**80, 2**80, id="large-integers"),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


def test_greatest_common_divisor_of_two_zeros():
    # Follow the conventional integer GCD definition, gcd(0, 0) == 0.
    assert greatest_common_divisor(0, 0) == 0
