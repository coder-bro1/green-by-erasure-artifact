"""Tests for the documented float-based Reverse Polish Notation calculator."""

import pytest

from solution import rpn_eval


def test_docstring_example():
    assert rpn_eval([3.0, 5.0, "+", 2.0, "/"]) == 4.0


@pytest.mark.parametrize("value", [0.0, 7.0, -3.5, 0.125])
def test_single_operand(value):
    assert rpn_eval([value]) == value


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        ([3.0, 5.0, "+"], 8.0),
        ([3.0, 5.0, "-"], -2.0),
        ([3.0, 5.0, "*"], 15.0),
        ([3.0, 5.0, "/"], 0.6),
        ([-3.0, 5.0, "+"], 2.0),
        ([-3.0, -5.0, "-"], 2.0),
        ([-3.0, 5.0, "*"], -15.0),
        ([-3.0, -5.0, "*"], 15.0),
        ([6.0, -4.0, "/"], -1.5),
        ([-6.0, -4.0, "/"], 1.5),
        ([0.0, 5.0, "+"], 5.0),
        ([0.0, 5.0, "-"], -5.0),
        ([5.0, 0.0, "*"], 0.0),
        ([0.0, 5.0, "/"], 0.0),
        ([0.1, 0.2, "+"], 0.3),
        ([5.5, 2.0, "/"], 2.75),
    ],
)
def test_binary_operations(tokens, expected):
    result = rpn_eval(tokens)
    assert isinstance(result, float)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        ([10.0, 3.0, "-", 2.0, "-"], 5.0),
        ([20.0, 2.0, "/", 5.0, "/"], 2.0),
        ([10.0, 3.0, 2.0, "-", "-"], 9.0),
        ([20.0, 10.0, 2.0, "/", "/"], 4.0),
        ([2.0, 3.0, "+", 4.0, 5.0, "+", "*"], 45.0),
        ([2.0, 3.0, 4.0, "*", "+"], 14.0),
        ([5.0, 1.0, 2.0, "+", 4.0, "*", "+", 3.0, "-"], 14.0),
        ([8.0, 2.0, "/", 3.0, "+", 2.0, "*", 5.0, "-"], 9.0),
    ],
)
def test_compound_expressions(tokens, expected):
    assert rpn_eval(tokens) == pytest.approx(expected)


def test_input_list_is_preserved():
    tokens = [3.0, 5.0, "+", 2.0, "/"]
    original = tokens.copy()

    assert rpn_eval(tokens) == 4.0
    assert tokens == original


def test_evaluations_have_independent_stacks():
    assert rpn_eval([2.0, 3.0, "+"]) == 5.0
    assert rpn_eval([8.0, 2.0, "/"]) == 4.0
    assert rpn_eval([1.0]) == 1.0
