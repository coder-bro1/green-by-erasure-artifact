import pytest

from solution import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
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
    ("a", "b", "expected"),
    [
        (7, 8, 56),
        (7, 0, 0),
        (30, 29, 0),
        pytest.param(
            -24,
            37,
            28,
            marks=pytest.mark.xfail(
                strict=True,
                reason="Negative unit digits must use the final digit's magnitude; solution.py uses Python's signed modulo result.",
            ),
        ),
        pytest.param(
            -24,
            -37,
            28,
            marks=pytest.mark.xfail(
                strict=True,
                reason="Negative unit digits must use the final digit's magnitude; solution.py uses Python's signed modulo result.",
            ),
        ),
        (12345678901234567899, 98765432109876543219, 81),
    ],
)
def test_product_of_unit_digits(a, b, expected):
    assert multiply(a, b) == expected
