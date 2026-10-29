import pytest

from solution import multiply

BUG = ("multiply() returns abs(a % 10) * abs(b % 10) * a * b; the extra '* a * b' "
       "factor means it does not return the product of the unit digits")


# Cases where the spurious '* a * b' factor is masked because a unit digit is 0.
@pytest.mark.parametrize("a, b, expected", [
    (2020, 1851, 0),   # docstring example
    (10, 7, 0),
    (0, 0, 0),
    (0, 123, 0),
    (-30, 45, 0),
])
def test_zero_unit_digit(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("a, b, expected", [
    (148, 412, 16),    # docstring example
    (19, 28, 72),      # docstring example
    (14, -15, 20),     # docstring example
])
def test_docstring_examples(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 1),
    (3, 4, 12),
    (9, 9, 81),
    (123, 456, 18),
    (-14, -15, 20),
    (-7, 3, 21),
])
def test_unit_digit_product(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
def test_result_is_bounded_by_81():
    # Product of two single digits can never exceed 81.
    assert multiply(99, 99) <= 81


@pytest.mark.xfail(strict=True, reason=BUG)
def test_commutative_and_symmetric_with_negation():
    assert multiply(37, 58) == multiply(58, 37) == multiply(-37, 58) == 56
