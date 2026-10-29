"""Tests for infix-to-RPN conversion and its currently known operator bug."""

import pytest

from solution import shunting_yard


@pytest.mark.parametrize(
    "tokens",
    [[], [0], [1], [-7], [10**100], [1, 2, 3], [-3, 0, 4, -3]],
    ids=["empty", "zero", "positive", "negative", "large", "integers", "duplicates"],
)
def test_integer_tokens_preserve_values_and_order(tokens):
    assert shunting_yard(tokens) == tokens


@pytest.mark.parametrize("tokens", [[], [1, 2, 3], [4, "+", 9, "*", 2]])
def test_does_not_mutate_input(tokens):
    original = tokens.copy()
    shunting_yard(tokens)
    assert tokens == original


def test_returns_independent_list_on_each_call():
    tokens = [7]
    first = shunting_yard(tokens)
    second = shunting_yard(tokens)
    assert first == second == [7]
    assert first is not tokens
    assert second is not tokens
    assert first is not second
    first.append(8)
    assert tokens == second == [7]


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Known bug: operators are never pushed onto opstack in solution.py",
)
@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([10, "-", 5, "-", 2], [10, 5, "-", 2, "-"]),
        ([34, "-", 12, "/", 5], [34, 12, 5, "/", "-"]),
        (
            [4, "+", 9, "*", 9, "-", 10, "+", 13],
            [4, 9, 9, "*", "+", 10, "-", 13, "+"],
        ),
        ([2, "+", 3], [2, 3, "+"]),
        ([2, "-", 3], [2, 3, "-"]),
        ([2, "*", 3], [2, 3, "*"]),
        ([2, "/", 3], [2, 3, "/"]),
        ([1, "+", 2, "-", 3], [1, 2, "+", 3, "-"]),
        ([1, "-", 2, "+", 3], [1, 2, "-", 3, "+"]),
        ([8, "*", 4, "/", 2], [8, 4, "*", 2, "/"]),
        ([8, "/", 4, "*", 2], [8, 4, "/", 2, "*"]),
        ([2, "+", 3, "*", 4], [2, 3, 4, "*", "+"]),
        ([2, "*", 3, "+", 4], [2, 3, "*", 4, "+"]),
        ([8, "-", 6, "/", 3], [8, 6, 3, "/", "-"]),
        ([8, "/", 4, "-", 2], [8, 4, "/", 2, "-"]),
    ],
    ids=[
        "doc-subtraction", "doc-division", "doc-mixed",
        "add", "subtract", "multiply", "divide",
        "add-subtract-left-associative", "subtract-add-left-associative",
        "multiply-divide-left-associative", "divide-multiply-left-associative",
        "multiply-after-add", "multiply-before-add",
        "divide-after-subtract", "divide-before-subtract",
    ],
)
def test_operator_conversion(tokens, expected):
    assert shunting_yard(tokens) == expected
