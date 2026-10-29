import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solution import multiply


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2020, 1851, 0),
        (0, 37, 0),
        (-20, 37, 0),
        (145, -30, 0),
    ],
)
def test_product_of_unit_digits_when_a_unit_digit_is_zero(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.xfail(
    strict=True,
    reason="multiply multiplies the full inputs in addition to their unit digits",
)
def test_documented_example_with_multi_digit_inputs():
    assert multiply(148, 412) == 16


@pytest.mark.xfail(
    strict=True,
    reason="multiply multiplies the full inputs in addition to their unit digits",
)
def test_documented_example_with_nonzero_unit_digits():
    assert multiply(19, 28) == 72


@pytest.mark.xfail(
    strict=True,
    reason="multiply multiplies the full inputs in addition to their unit digits",
)
def test_documented_example_with_negative_input():
    assert multiply(14, -15) == 20


@pytest.mark.xfail(
    strict=True,
    reason="multiply multiplies the full inputs in addition to their unit digits",
)
def test_single_digit_inputs():
    assert multiply(7, 8) == 56


@pytest.mark.xfail(
    strict=True,
    reason="multiply multiplies the full inputs in addition to their unit digits",
)
def test_negative_multi_digit_inputs_use_absolute_unit_digits():
    assert multiply(-24, -13) == 12
