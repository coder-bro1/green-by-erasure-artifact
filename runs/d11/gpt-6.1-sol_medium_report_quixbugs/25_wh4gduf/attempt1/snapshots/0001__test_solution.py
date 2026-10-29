"""Tests for the documented infix-to-RPN conversion contract."""

import pytest

from solution import shunting_yard


@pytest.mark.parametrize(
    ("tokens", "expected"),
    [
        pytest.param([10, "-", 5, "-", 2], [10, 5, "-", 2, "-"], id="example-subtraction"),
        pytest.param([34, "-", 12, "/", 5], [34, 12, 5, "/", "-"], id="example-division"),
        pytest.param(
            [4, "+", 9, "*", 9, "-", 10, "+", 13],
            [4, 9, 9, "*", "+", 10, "-", 13, "+"],
            id="example-mixed-expression",
        ),
        pytest.param([], [], id="empty-input"),
        pytest.param([0], [0], id="single-zero"),
        pytest.param([-7], [-7], id="single-negative-integer"),
        pytest.param([10**100], [10**100], id="large-integer"),
        pytest.param([0, "+", -7], [0, -7, "+"], id="negative-operand"),
        pytest.param([2, "+", 3, "+", 4], [2, 3, "+", 4, "+"], id="addition-left-associative"),
        pytest.param([2, "*", 3, "*", 4], [2, 3, "*", 4, "*"], id="multiplication-left-associative"),
        pytest.param([24, "/", 4, "/", 2], [24, 4, "/", 2, "/"], id="division-left-associative"),
        pytest.param([8, "+", 3, "-", 2], [8, 3, "+", 2, "-"], id="addition-then-subtraction"),
        pytest.param([8, "-", 3, "+", 2], [8, 3, "-", 2, "+"], id="subtraction-then-addition"),
        pytest.param([8, "*", 3, "/", 2], [8, 3, "*", 2, "/"], id="multiplication-then-division"),
        pytest.param([8, "/", 2, "*", 3], [8, 2, "/", 3, "*"], id="division-then-multiplication"),
        pytest.param([2, "+", 3, "*", 4], [2, 3, 4, "*", "+"], id="multiplication-before-addition"),
        pytest.param([8, "+", 6, "/", 2], [8, 6, 2, "/", "+"], id="division-before-addition"),
        pytest.param([8, "-", 3, "*", 2], [8, 3, 2, "*", "-"], id="multiplication-before-subtraction"),
        pytest.param([2, "*", 3, "+", 4], [2, 3, "*", 4, "+"], id="multiplication-before-following-addition"),
        pytest.param([8, "/", 2, "-", 3], [8, 2, "/", 3, "-"], id="division-before-following-subtraction"),
        pytest.param(
            [1, "+", 2, "*", 3, "/", 4, "-", 5],
            [1, 2, 3, "*", 4, "/", "+", 5, "-"],
            id="flush-multiple-pending-operators",
        ),
        pytest.param(
            [1, "+", 2, "*", 3, "-", 4, "/", 5],
            [1, 2, 3, "*", "+", 4, 5, "/", "-"],
            id="flush-stack-at-end",
        ),
    ],
)
def test_shunting_yard_documented_conversion(tokens, expected):
    original = tokens.copy()

    result = shunting_yard(tokens)

    assert isinstance(result, list)
    assert result == expected
    assert tokens == original


@pytest.mark.parametrize("operator", ["+", "-", "*", "/"])
def test_each_binary_operator(operator):
    assert shunting_yard([12, operator, 3]) == [12, 3, operator]


def test_repeated_calls_have_independent_results():
    first = shunting_yard([1, "+", 2])
    first.append(99)

    assert shunting_yard([1, "+", 2]) == [1, 2, "+"]
    assert shunting_yard([6, "/", 3]) == [6, 3, "/"]
    assert shunting_yard([]) == []
