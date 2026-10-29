import pytest

from solution import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        pytest.param(148, 412, 16, id="documented-positive-example"),
        pytest.param(19, 28, 72, id="documented-nine-and-eight"),
        pytest.param(2020, 1851, 0, id="documented-trailing-zero"),
        pytest.param(14, -15, 20, id="documented-negative-example"),
        pytest.param(0, 123, 0, id="zero-first"),
        pytest.param(123, 0, 0, id="zero-second"),
        pytest.param(0, 0, 0, id="both-zero"),
        pytest.param(3, 7, 21, id="single-digits"),
        pytest.param(1, 1, 1, id="ones"),
        pytest.param(99, 99, 81, id="maximum-product"),
        pytest.param(-12, 34, 8, id="negative-first"),
        pytest.param(12, -34, 8, id="negative-second"),
        pytest.param(-12, -34, 8, id="both-negative"),
        pytest.param(-3, -7, 21, id="negative-single-digits"),
        pytest.param(-120, -34, 0, id="negative-trailing-zero"),
        pytest.param(123, 450, 0, id="trailing-zero-second"),
        pytest.param(10**100 + 7, -(10**100 + 8), 56, id="large-integers"),
    ],
)
def test_multiply_returns_product_of_absolute_unit_digits(a, b, expected):
    assert multiply(a, b) == expected
