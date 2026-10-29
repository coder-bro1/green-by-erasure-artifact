import pytest

from solution import last_digit_product


# Examples taken directly from the docstring (the specification).
@pytest.mark.parametrize(
    "x, y, expected",
    [
        (37, 54, 28),
        (-21, 46, 54),
        (1990, 13, 0),
    ],
)
def test_docstring_examples(x, y, expected):
    assert last_digit_product(x, y) == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (1, 1, 1),
        (9, 9, 81),
        (12, 3, 6),
        (123456789, 987654321, 9),
        (10**20 + 7, 8, 56),
    ],
)
def test_positive_values(x, y, expected):
    assert last_digit_product(x, y) == expected


@pytest.mark.parametrize("x, y", [(0, 5), (5, 0), (0, 0), (10, 99), (47, 100)])
def test_zero_last_digit_gives_zero(x, y):
    assert last_digit_product(x, y) == 0


@pytest.mark.parametrize("x, y", [(37, 54), (1990, 13), (8, 7), (123, 456)])
def test_commutative(x, y):
    assert last_digit_product(x, y) == last_digit_product(y, x)


@pytest.mark.parametrize("x, y", [(37, 54), (8, 7), (123, 456), (99, 99)])
def test_result_in_digit_product_range(x, y):
    result = last_digit_product(x, y)
    assert 0 <= result <= 81


def test_returns_int():
    assert isinstance(last_digit_product(37, 54), int)
