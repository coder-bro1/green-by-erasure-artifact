import pytest

from solution import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (148, 412, 16),
        (19, 28, 72),
        (2020, 1851, 0),
        (14, -15, 20),
        (-19, 28, 72),
        (-19, -28, 72),
        (0, -987, 0),
        (7, 3, 21),
        (12345678901234567890, 98765432109876543219, 90),
    ],
)
def test_multiply_returns_product_of_unit_digits(a, b, expected):
    assert multiply(a, b) == expected


def test_multiply_is_commutative():
    assert multiply(237, -48) == multiply(-48, 237)
