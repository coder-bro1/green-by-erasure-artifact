"""Tests for the documented parentheses-only input contract."""

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
        "()(())",
        "(())()",
        "((()()))()",  # Documented valid example.
        "(" * 1000 + ")" * 1000,
        "()" * 1000,
    ],
)
def test_accepts_balanced_parentheses(parens):
    assert is_valid_parenthesization(parens) is True


@pytest.mark.parametrize(
    "parens",
    [
        ")",
        "))",
        ")(",
        ")()(",  # Documented invalid example; equal counts are insufficient.
        "())",
        "())(",
        "(()))",
        "()())(()",
        ")" + "()" * 1000,
        "(" * 1000 + ")" * 1001,
    ],
)
def test_rejects_closing_parenthesis_without_matching_open(parens):
    assert is_valid_parenthesization(parens) is False


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: the function does not check for unmatched opening parentheses.",
)
@pytest.mark.parametrize("parens", ["(", "((", "(()", "()(", "(" * 1000])
def test_rejects_unmatched_opening_parentheses(parens):
    assert is_valid_parenthesization(parens) is False
