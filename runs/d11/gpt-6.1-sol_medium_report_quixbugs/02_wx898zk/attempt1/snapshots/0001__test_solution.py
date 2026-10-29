import pytest

from solution import shunting_yard


@pytest.mark.parametrize("tokens", [[], [0], [42], [-7], [10**100]])
def test_empty_expression_and_single_integer(tokens):
    assert shunting_yard(tokens) == tokens


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([10, "-", 5, "-", 2], [10, 5, "-", 2, "-"]),
        ([34, "-", 12, "/", 5], [34, 12, 5, "/", "-"]),
        (
            [4, "+", 9, "*", 9, "-", 10, "+", 13],
            [4, 9, 9, "*", "+", 10, "-", 13, "+"],
        ),
    ],
    ids=["subtraction", "division-precedence", "mixed-chain"],
)
def test_docstring_examples(tokens, expected):
    assert shunting_yard(tokens) == expected


@pytest.mark.parametrize("operator", ["+", "-", "*", "/"])
def test_single_operator(operator):
    assert shunting_yard([8, operator, 2]) == [8, 2, operator]


@pytest.mark.parametrize(
    "first, second",
    [
        ("+", "+"), ("+", "-"), ("-", "+"), ("-", "-"),
        ("*", "*"), ("*", "/"), ("/", "*"), ("/", "/"),
    ],
)
def test_equal_precedence_is_left_associative(first, second):
    assert shunting_yard([20, first, 5, second, 2]) == [
        20, 5, first, 2, second
    ]


@pytest.mark.parametrize("low", ["+", "-"])
@pytest.mark.parametrize("high", ["*", "/"])
@pytest.mark.parametrize("high_first", [False, True])
def test_multiplication_and_division_precede_addition_and_subtraction(
    low, high, high_first
):
    if high_first:
        tokens = [12, high, 3, low, 2]
        expected = [12, 3, high, 2, low]
    else:
        tokens = [12, low, 3, high, 2]
        expected = [12, 3, 2, high, low]
    assert shunting_yard(tokens) == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([0, "+", -3, "*", -2], [0, -3, -2, "*", "+"]),
        ([10**100, "-", 1], [10**100, 1, "-"]),
        # Conversion reorders tokens; it does not evaluate division by zero.
        ([1, "/", 0], [1, 0, "/"]),
        (
            [1, "+", 2, "*", 3, "-", 4, "/", 5],
            [1, 2, 3, "*", "+", 4, 5, "/", "-"],
        ),
    ],
    ids=["signed-integers", "large-integer", "zero-divisor", "all-operators"],
)
def test_integer_values_and_long_expression(tokens, expected):
    assert shunting_yard(tokens) == expected


def test_conversion_does_not_mutate_input():
    tokens = [4, "+", 9, "*", 2]
    original = tokens.copy()
    result = shunting_yard(tokens)
    assert tokens == original
    assert result is not tokens
