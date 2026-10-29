"""Tests for the current behavior of the RPN evaluator."""

import pytest

from solution import rpn_eval


@pytest.mark.parametrize("value", [0.0, 3.5, -7.25])
def test_single_value(value):
    assert rpn_eval([value]) == value


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        ([3.0, 5.0, "+"], 8.0),
        ([3.0, 5.0, "*"], 15.0),
        ([-3.0, 5.0, "+"], 2.0),
        ([-3.0, -5.0, "*"], 15.0),
        ([0.0, 5.0, "*"], 0.0),
        ([0.1, 0.2, "+"], 0.3),
    ],
)
def test_addition_and_multiplication(tokens, expected):
    assert rpn_eval(tokens) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        ([3.0, 5.0, "-"], 2.0),
        ([5.0, 3.0, "-"], -2.0),
        ([2.0, 8.0, "/"], 4.0),
        ([8.0, 2.0, "/"], 0.25),
        ([-2.0, 8.0, "/"], -4.0),
        ([2.0, 0.0, "/"], 0.0),
    ],
)
def test_noncommutative_operators_use_top_of_stack_as_left_operand(tokens, expected):
    # The implementation computes last-pushed operand OP previous operand.
    assert rpn_eval(tokens) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        ([2.0, 3.0, "+", 4.0, "*"], 20.0),
        ([2.0, 3.0, "+", 4.0, 5.0, "+", "*"], 45.0),
        ([2.0, 8.0, "/", 3.0, "-"], -1.0),
        ([1.0, 2.0, 3.0, "*", "+"], 7.0),
    ],
)
def test_multiple_operations(tokens, expected):
    assert rpn_eval(tokens) == pytest.approx(expected)


def test_input_list_is_not_modified():
    tokens = [2.0, 3.0, "+", 4.0, "*"]
    original = tokens.copy()

    assert rpn_eval(tokens) == 20.0
    assert tokens == original


def test_returns_top_value_when_unused_operands_remain():
    assert rpn_eval([1.0, 2.0, 3.0, "+"]) == 5.0


@pytest.mark.parametrize("tokens", [[], ["+"], [1.0, "*"], [1.0, 2.0, "+", "/"]])
def test_insufficient_operands_raise_index_error(tokens):
    with pytest.raises(IndexError):
        rpn_eval(tokens)


def test_zero_divisor_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        rpn_eval([0.0, 2.0, "/"])
