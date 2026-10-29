import pytest
from solution import multiply


@pytest.mark.parametrize("a, b, expected", [
    # Docstring examples
    (148, 412, 16),
    (19, 28, 72),
    (2020, 1851, 0),
    (14, -15, 20),
    # Additional cases
    (0, 0, 0),
    (0, 7, 0),
    (5, 5, 25),
    (9, 9, 81),
    (1, 1, 1),
    (10, 99, 0),
    (123456789, 987654321, 9),
    (-15, 14, 20),
    (-15, -15, 25),
])
def test_multiply_unit_digits(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    # Unit digit of a negative number is the unit digit of its absolute value
    (-13, 7, 21),
    (-12, -14, 8),
    (-1, 2, 2),
])
def test_multiply_negative_unit_digits(a, b, expected):
    assert multiply(a, b) == expected


def test_multiply_is_commutative():
    for a, b in [(148, 412), (19, 28), (14, -15), (-37, 46)]:
        assert multiply(a, b) == multiply(b, a)


def test_result_range():
    for a in range(-30, 31):
        for b in range(-30, 31):
            assert 0 <= multiply(a, b) <= 81
