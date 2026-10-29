import pytest

from solution import multiply


@pytest.mark.parametrize(
    "a, b, expected",
    [
        pytest.param(148, 412, 16, id="example-1"),
        pytest.param(19, 28, 72, id="example-2"),
        pytest.param(2020, 1851, 0, id="example-3"),
        pytest.param(14, -15, 20, id="example-4"),
        pytest.param(0, 0, 0, id="both-zero"),
        pytest.param(0, 123, 0, id="first-zero"),
        pytest.param(456, 0, 0, id="second-zero"),
        pytest.param(120, 789, 0, id="first-trailing-zero"),
        pytest.param(789, -120, 0, id="negative-trailing-zero"),
        pytest.param(7, 8, 56, id="single-digit"),
        pytest.param(99, 999, 81, id="maximum-product"),
        pytest.param(-14, 23, 12, id="negative-first"),
        pytest.param(23, -14, 12, id="negative-second"),
        pytest.param(-17, -28, 56, id="both-negative"),
        pytest.param(-1, 9, 9, id="negative-single-digit"),
        pytest.param(10**100 + 7, -(10**100 + 8), 56, id="large-integers"),
    ],
)
def test_multiply_unit_digits(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a", range(-9, 10))
@pytest.mark.parametrize("b", range(-9, 10))
def test_multiply_all_signed_single_digits(a, b):
    assert multiply(a, b) == abs(a * b)
