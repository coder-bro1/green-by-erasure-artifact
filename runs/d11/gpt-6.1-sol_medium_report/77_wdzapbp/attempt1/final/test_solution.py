import pytest

from solution import multiply


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2020, 1851, 0),  # Documented example.
        (0, 0, 0),
        (0, 123, 0),
        (-123, 0, 0),
        (10, 99, 0),
        (99, 10, 0),
        (-20, -99, 0),
        (-99, -20, 0),
        (1, 1, 1),
    ],
)
def test_multiply_zero_unit_digits_and_identity(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.xfail(
    strict=True,
    reason="multiply incorrectly multiplies the unit-digit product by a * b",
)
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (148, 412, 16),
        (19, 28, 72),
        (14, -15, 20),
    ],
)
def test_multiply_documented_nonzero_examples(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.xfail(
    strict=True,
    reason=(
        "multiply incorrectly multiplies by a * b and uses abs(a % 10) "
        "instead of abs(a) % 10 for negative inputs"
    ),
)
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (9, 9, 81),
        (11, 21, 1),
        (123456789, 987654321, 9),
        (-12, 13, 6),
        (12, -13, 6),
        (-12, -13, 6),
        (-1, 1, 1),
        (1, -1, 1),
        (-1, -1, 1),
        (10**100 + 7, 10**100 + 8, 56),
        (-(10**100 + 7), 10**100 + 8, 56),
    ],
)
def test_multiply_unit_digits_across_sizes_and_signs(a, b, expected):
    assert multiply(a, b) == expected
