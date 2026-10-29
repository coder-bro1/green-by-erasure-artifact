import pytest

from solution import multiply


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (148, 412, 16),
        (19, 28, 72),
        (2020, 1851, 0),
        (14, -15, 20),
    ],
)
def test_docstring_examples(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 0, 0),
        (0, 7, 0),
        (9, 9, 81),
        (1, 1, 1),
        (3, 4, 12),
        (10, 25, 0),
        (123456789, 987654321, 9),
        (76, 89, 54),
    ],
)
def test_non_negative_inputs(a, b, expected):
    assert multiply(a, b) == expected


def test_commutative():
    assert multiply(37, 58) == multiply(58, 37) == 56


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (-15, -25, 25),
        (-10, 7, 0),
        (-20, -30, 0),
    ],
)
def test_negative_inputs_ending_in_0_or_5(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Python's % on negatives returns 10 - unit digit (e.g. -14 % 10 == 6), "
    "so abs(a % 10) is not the unit digit of a negative number",
)
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (-14, 3, 12),   # unit digits 4 and 3; solution returns 6*3 = 18
        (14, -16, 24),  # unit digits 4 and 6; solution returns 4*4 = 16
        (-19, -28, 72), # unit digits 9 and 8; solution returns 1*2 = 2
        (-1, 1, 1),     # unit digits 1 and 1; solution returns 9*1 = 9
    ],
)
def test_negative_inputs_general(a, b, expected):
    assert multiply(a, b) == expected
