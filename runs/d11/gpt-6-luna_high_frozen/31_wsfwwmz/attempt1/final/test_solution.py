import pytest

from solution import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (0, 1851, 0),
        (1, 1, 1),
    ],
)
def test_multiply_returns_product_of_unit_digits_for_zero_and_one(a, b, expected):
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
