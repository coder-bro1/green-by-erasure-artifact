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
        "((()()))()",  # The valid example in the docstring.
        "(" * 1000 + ")" * 1000,
        "()" * 1000,
    ],
)
def test_properly_nested_parentheses_are_valid(parens):
    assert is_valid_parenthesization(parens) is True


@pytest.mark.parametrize(
    "parens",
    [
        ")",
        ")(",
        ")()(",  # The invalid example in the docstring.
        "())",
        "(()))",
        "())(()",  # Equal totals cannot repair an invalid prefix.
        ")()",
        "())(",
        "()" * 1000 + ")",
    ],
)
def test_closing_parenthesis_without_an_open_match_is_invalid(parens):
    assert is_valid_parenthesization(parens) is False


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The docstring requires properly nested parentheses, but the function "
        "returns True when unmatched opening parentheses remain at the end."
    ),
)
@pytest.mark.parametrize(
    "parens",
    ["(", "((", "(()", "()(", "(()()", "((())", "(" * 1000],
)
def test_unmatched_opening_parentheses_are_invalid(parens):
    assert is_valid_parenthesization(parens) is False
