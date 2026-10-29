import pytest

from solution import rpn_eval


@pytest.mark.parametrize("value", [0.0, 7.5, -3.25])
def test_single_operand(value):
    assert rpn_eval([value]) == value


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([3.0, 5.0, "+"], 8.0),
        ([-3.0, 5.0, "+"], 2.0),
        ([0.1, 0.2, "+"], 0.3),
        ([3.0, 5.0, "*"], 15.0),
        ([-3.0, 5.0, "*"], -15.0),
        ([0.0, 5.0, "*"], 0.0),
        ([1.5, 2.5, "*"], 3.75),
        ([2.0, 3.0, "+", 4.0, "*"], 20.0),
        ([2.0, 3.0, 4.0, "*", "+"], 14.0),
        ([2.0, 3.0, "+", 4.0, 5.0, "+", "*"], 45.0),
        ([6.0, 6.0, "-"], 0.0),
        ([6.0, 6.0, "/"], 1.0),
    ],
)
def test_arithmetic_and_stack_evaluation(tokens, expected):
    assert rpn_eval(tokens) == pytest.approx(expected)


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([8.0, 3.0, "-"], 5.0),
        ([3.0, 8.0, "-"], -5.0),
        ([-8.0, -3.0, "-"], -5.0),
    ],
)
def test_subtraction_operand_order(tokens, expected):
    assert rpn_eval(tokens) == pytest.approx(expected)


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([8.0, 2.0, "/"], 4.0),
        ([2.0, 8.0, "/"], 0.25),
        ([-9.0, 2.0, "/"], -4.5),
    ],
)
def test_division_operand_order(tokens, expected):
    assert rpn_eval(tokens) == pytest.approx(expected)


def test_docstring_example():
    assert rpn_eval([3.0, 5.0, "+", 2.0, "/"]) == 4.0


def test_input_list_is_preserved():
    tokens = [2.0, 3.0, "+", 4.0, "*"]
    original = tokens.copy()
    assert rpn_eval(tokens) == 20.0
    assert tokens == original


def test_calls_have_independent_stacks():
    assert rpn_eval([2.0, 3.0, "+"]) == 5.0
    assert rpn_eval([4.0]) == 4.0
    assert rpn_eval([5.0, 6.0, "*"]) == 30.0
