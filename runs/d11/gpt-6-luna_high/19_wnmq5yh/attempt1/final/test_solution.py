import pytest

from solution import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (148, 412, 16),
        (19, 28, 72),
        (2020, 1851, 0),
        (14, -15, 20),
        (-14, 15, 20),
        (-14, -15, 20),
        (0, 123, 0),
        (7, 8, 56),
        (1000000009, 2000000008, 72),
    ],
)
def test_multiply_returns_product_of_unit_digits(a, b, expected):
    assert multiply(a, b) == expected
