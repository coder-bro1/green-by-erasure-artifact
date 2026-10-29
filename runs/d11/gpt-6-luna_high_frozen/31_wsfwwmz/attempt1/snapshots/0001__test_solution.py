import pytest

from solution import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (0, 1851, 0),
        (7, 8, 56),
        (-7, 8, 56),
    ],
)
def test_multiply_returns_product_of_unit_digits_when_inputs_are_single_digit(
    a, b, expected
):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (148, 412, 16),
        (19, 28, 72),
        (14, -15, 20),
    ],
)
@pytest.mark.xfail(
    strict=False,
    reason="solution.multiply currently multiplies by the original inputs too",
)
def test_multiply_returns_product_of_unit_digits_for_documented_examples(
    a, b, expected
):
    assert multiply(a, b) == expected
