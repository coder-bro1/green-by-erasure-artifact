"""Tests for the documented parentheses-only input contract."""

from itertools import product

import pytest

from solution import is_valid_parenthesization


@pytest.mark.parametrize(
    "parens",
    [
        "",
        "()",
        "(())",
        "()()",
        "(()())",
        "((()()))()",  # Docstring example.
        "()(())(()())",
        "(" * 1000 + ")" * 1000,
        "()" * 1000,
    ],
)
def test_properly_nested_parentheses(parens):
    assert is_valid_parenthesization(parens) is True


@pytest.mark.parametrize(
    "parens",
    [
        "(",
        ")",
        "((",
        "))",
        "(()",
        "())",
        ")(",
        ")()(",  # Docstring example.
        "())(",
        "(()))(",
        "()()(",
        ")()()",
        "(" * 1000 + ")" * 999,
        "(" * 999 + ")" * 1000,
    ],
)
def test_improperly_nested_parentheses(parens):
    assert is_valid_parenthesization(parens) is False


def reduces_to_empty(parens):
    """A balanced string can be reduced by removing adjacent matched pairs."""
    while "()" in parens:
        parens = parens.replace("()", "")
    return parens == ""


@pytest.mark.parametrize("length", range(11))
def test_all_short_parentheses_strings(length):
    for characters in product("()", repeat=length):
        parens = "".join(characters)
        assert is_valid_parenthesization(parens) is reduces_to_empty(parens), parens
