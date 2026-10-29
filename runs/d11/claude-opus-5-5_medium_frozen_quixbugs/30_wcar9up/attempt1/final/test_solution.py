import math

import pytest

from solution import rpn_eval

# Known defect in solution.py: operands are passed to the operator in the
# wrong order (op(token, a, b) where `a` is the top of the stack), so
# non-commutative operators ('-' and '/') compute `right OP left`.
# Tests that encode the documented behaviour for those operators are marked
# strict xfail: they document the bug and will flag (XPASS -> failure) once
# solution.py is fixed, so the markers can be removed.
OPERAND_ORDER_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py swaps operands for non-commutative operators",
)


# --- Behaviour that is correct in the current implementation ---------------

def test_single_number_returns_itself():
    assert rpn_eval([42.0]) == 42.0


def test_addition():
    assert rpn_eval([3.0, 5.0, '+']) == 8.0


def test_multiplication():
    assert rpn_eval([4.0, 2.5, '*']) == 10.0


def test_chained_commutative_operations():
    # (1 + 2) * (3 + 4) = 21
    assert rpn_eval([1.0, 2.0, '+', 3.0, 4.0, '+', '*']) == 21.0


def test_negative_and_fractional_values():
    assert rpn_eval([-1.5, 0.5, '+']) == -1.0
    assert rpn_eval([-2.0, -3.0, '*']) == 6.0


def test_subtraction_of_equal_values_is_zero():
    assert rpn_eval([7.0, 7.0, '-']) == 0.0


def test_division_of_equal_values_is_one():
    assert rpn_eval([9.0, 9.0, '/']) == 1.0


def test_returns_top_of_stack_when_extra_values_remain():
    assert rpn_eval([1.0, 2.0, 3.0]) == 3.0


def test_does_not_mutate_input():
    tokens = [3.0, 5.0, '+']
    rpn_eval(tokens)
    assert tokens == [3.0, 5.0, '+']


def test_float_special_values():
    assert math.isinf(rpn_eval([float('inf'), 1.0, '+']))
    assert math.isnan(rpn_eval([float('nan'), 1.0, '*']))


def test_empty_input_raises():
    with pytest.raises(IndexError):
        rpn_eval([])


def test_operator_without_enough_operands_raises():
    with pytest.raises(IndexError):
        rpn_eval([1.0, '+'])
    with pytest.raises(IndexError):
        rpn_eval(['*'])


def test_unknown_operator_raises():
    with pytest.raises(KeyError):
        rpn_eval([1.0, 2.0, '^'])


def test_integer_tokens_are_treated_as_operators():
    # Precondition requires floats; an int is not pushed as a value.
    with pytest.raises(IndexError):
        rpn_eval([1, 2, '+'])


def test_division_by_zero_raises():
    # Division by zero results in either operand order here.
    with pytest.raises(ZeroDivisionError):
        rpn_eval([0.0, 0.0, '/'])


# --- Documented behaviour that the current implementation gets wrong ------

@OPERAND_ORDER_BUG
def test_docstring_example():
    assert rpn_eval([3.0, 5.0, '+', 2.0, '/']) == 4.0


@OPERAND_ORDER_BUG
def test_subtraction_operand_order():
    assert rpn_eval([5.0, 3.0, '-']) == 2.0


@OPERAND_ORDER_BUG
def test_division_operand_order():
    assert rpn_eval([6.0, 2.0, '/']) == 3.0


@OPERAND_ORDER_BUG
def test_mixed_expression():
    # (5 + ((1 + 2) * 4)) - 3 = 14
    assert rpn_eval([5.0, 1.0, 2.0, '+', 4.0, '*', '+', 3.0, '-']) == 14.0


@OPERAND_ORDER_BUG
def test_division_by_zero_divisor():
    with pytest.raises(ZeroDivisionError):
        rpn_eval([1.0, 0.0, '/'])
