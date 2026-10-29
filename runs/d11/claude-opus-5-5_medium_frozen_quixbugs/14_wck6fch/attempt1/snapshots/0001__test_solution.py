import pytest

from solution import shunting_yard

# NOTE: solution.py has a known bug: the operator branch never pushes the
# current token onto `opstack` (missing `opstack.append(token)`), so every
# operator is silently dropped. Tests that depend on operators being emitted
# are marked xfail(strict=True): they document the correct, specified
# behaviour and will start failing loudly (XPASS -> error) once the bug is
# fixed, signalling that the marker should be removed.
BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py never pushes operators onto opstack (missing opstack.append(token))",
)


# ---------------------------------------------------------------------------
# Behaviour that works correctly with the current implementation
# ---------------------------------------------------------------------------

def test_empty_input():
    assert shunting_yard([]) == []


def test_single_operand():
    assert shunting_yard([42]) == [42]


def test_operands_only_preserve_order():
    assert shunting_yard([1, 2, 3]) == [1, 2, 3]


def test_zero_and_negative_ints_are_operands():
    assert shunting_yard([0]) == [0]
    assert shunting_yard([-7]) == [-7]


def test_does_not_mutate_input():
    tokens = [1, '+', 2, '*', 3]
    original = list(tokens)
    shunting_yard(tokens)
    assert tokens == original


def test_returns_new_list():
    tokens = [5]
    result = shunting_yard(tokens)
    assert result == tokens
    assert result is not tokens


def test_operands_appear_in_original_order():
    # Shunting-yard never reorders operands relative to each other.
    tokens = [4, '+', 9, '*', 9, '-', 10, '+', 13]
    result = shunting_yard(tokens)
    assert [t for t in result if isinstance(t, int)] == [4, 9, 9, 10, 13]


# ---------------------------------------------------------------------------
# Specified behaviour (docstring + standard algorithm) -- currently broken
# ---------------------------------------------------------------------------

@BUG
@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([10, '-', 5, '-', 2], [10, 5, '-', 2, '-']),
        ([34, '-', 12, '/', 5], [34, 12, 5, '/', '-']),
        ([4, '+', 9, '*', 9, '-', 10, '+', 13], [4, 9, 9, '*', '+', 10, '-', 13, '+']),
    ],
)
def test_docstring_examples(tokens, expected):
    assert shunting_yard(tokens) == expected


@BUG
@pytest.mark.parametrize("op", ['+', '-', '*', '/'])
def test_single_binary_operation(op):
    assert shunting_yard([1, op, 2]) == [1, 2, op]


@BUG
def test_higher_precedence_on_right():
    assert shunting_yard([1, '+', 2, '*', 3]) == [1, 2, 3, '*', '+']


@BUG
def test_higher_precedence_on_left():
    assert shunting_yard([1, '*', 2, '+', 3]) == [1, 2, '*', 3, '+']


@BUG
def test_left_associativity_same_precedence():
    assert shunting_yard([8, '/', 4, '/', 2]) == [8, 4, '/', 2, '/']
    assert shunting_yard([1, '+', 2, '-', 3]) == [1, 2, '+', 3, '-']


@BUG
def test_mixed_chain():
    assert shunting_yard([1, '*', 2, '+', 3, '*', 4]) == [1, 2, '*', 3, 4, '*', '+']


@BUG
def test_output_contains_all_tokens():
    tokens = [3, '-', 4, '*', 5, '/', 6, '+', 7]
    result = shunting_yard(tokens)
    assert sorted(map(str, result)) == sorted(map(str, tokens))


# ---------------------------------------------------------------------------
# Semantic check: evaluating the RPN gives the same value as Python's infix
# ---------------------------------------------------------------------------

def _eval_rpn(rpn):
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
    }
    for tok in rpn:
        if isinstance(tok, int):
            stack.append(tok)
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[tok](a, b))
    assert len(stack) == 1
    return stack[0]


@BUG
@pytest.mark.parametrize(
    "tokens",
    [
        [2, '+', 3, '*', 4, '-', 5],
        [100, '/', 10, '/', 2, '+', 1],
        [7, '-', 2, '-', 1, '*', 3],
    ],
)
def test_rpn_evaluates_to_infix_value(tokens):
    expr = " ".join(map(str, tokens))
    assert _eval_rpn(shunting_yard(tokens)) == pytest.approx(eval(expr))
