"""Regression tests for the current implementation, which differs from its docstring."""

import pytest

from solution import last_digit_product


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (1, 1, 1),
        (9, 9, 6561),
        (37, 54, 55944),
        (54, 37, 55944),
        (12, 23, 1656),
        (-21, 46, -52164),
        (21, -46, -3864),
        (-21, -46, 34776),
        (-1, 1, -9),
        (-1, -1, 81),
    ],
)
def test_current_results(x, y, expected):
    # These expectations preserve existing behavior, not the docstring examples.
    assert last_digit_product(x, y) == expected


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (0, 0),
        (0, 17),
        (17, 0),
        (1990, 13),
        (13, 1990),
        (-10, 17),
        (17, -10),
        (-20, -30),
    ],
)
def test_zero_or_trailing_zero_produces_zero(x, y):
    assert last_digit_product(x, y) == 0


def test_arbitrary_precision_integers():
    magnitude = 10**100
    expected = 28 * 10**200 + 308 * 10**100 + 784
    assert last_digit_product(magnitude + 7, magnitude + 4) == expected


@pytest.mark.parametrize(("x", "y"), [(None, 3), (3, None), ("12", 3), (3, "12")])
def test_unsupported_inputs_raise_type_error(x, y):
    with pytest.raises(TypeError):
        last_digit_product(x, y)
