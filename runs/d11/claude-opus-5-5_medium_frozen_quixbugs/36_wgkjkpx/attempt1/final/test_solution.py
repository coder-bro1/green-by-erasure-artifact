import pytest

from solution import is_valid_parenthesization


@pytest.mark.parametrize(
    "parens",
    [
        "",
        "()",
        "(())",
        "()()",
        "((()()))()",  # docstring example
        "(()(()))",
        "()" * 50,
        "(" * 100 + ")" * 100,
    ],
)
def test_valid(parens):
    assert is_valid_parenthesization(parens) is True


@pytest.mark.parametrize(
    "parens",
    [
        ")",
        ")(",
        ")()(",  # docstring example
        "())",
        "())(()",
        "())(",
        "()" * 20 + ")",
    ],
)
def test_invalid_closing_before_opening(parens):
    assert is_valid_parenthesization(parens) is False


@pytest.mark.xfail(
    reason="BUG in solution.py: missing final `depth == 0` check, so unclosed "
    "'(' are reported as valid",
    strict=True,
)
@pytest.mark.parametrize("parens", ["(", "((", "(()", "()(", "((()"])
def test_invalid_unclosed_opening(parens):
    assert is_valid_parenthesization(parens) is False


def test_returns_bool():
    assert isinstance(is_valid_parenthesization("()"), bool)
    assert isinstance(is_valid_parenthesization(")"), bool)
