import pytest

from solution import multiply


@pytest.mark.parametrize(
    "a,b,expected",
    [
        pytest.param(148, 412, 16, id="example-multiple-digits"),
        pytest.param(19, 28, 72, id="example-nine-times-eight"),
        pytest.param(2020, 1851, 0, id="example-trailing-zero"),
        pytest.param(14, -15, 20, id="example-negative-input"),
        pytest.param(3, 7, 21, id="single-digit-inputs"),
        pytest.param(1, 1, 1, id="unit-inputs"),
        pytest.param(0, 123, 0, id="zero-first"),
        pytest.param(123, 0, 0, id="zero-second"),
        pytest.param(0, 0, 0, id="both-zero"),
        pytest.param(-12, 13, 6, id="negative-first"),
        pytest.param(12, -13, 6, id="negative-second"),
        pytest.param(-12, -13, 6, id="both-negative"),
        pytest.param(-10, -19, 0, id="negative-trailing-zero"),
        pytest.param(123456789, 987654321, 9, id="ignore-leading-digits"),
        pytest.param(10**100 + 7, 10**100 + 8, 56, id="arbitrary-size-integers"),
    ],
)
def test_multiply_unit_digits(a, b, expected):
    """Return the product of the magnitudes of the two unit digits."""
    assert multiply(a, b) == expected
