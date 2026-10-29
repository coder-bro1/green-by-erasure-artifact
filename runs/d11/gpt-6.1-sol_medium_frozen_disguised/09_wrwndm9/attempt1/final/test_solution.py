"""Regression tests for the current lowercase-only implementation.

The solution's docstring describes case swapping, but its implementation uses
str.lower(). These tests record actual behavior without changing solution.py.
"""

import pytest

from solution import invert_letter_case


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("python", "python", id="lowercase-unchanged"),
        pytest.param("PYTHON", "python", id="uppercase-lowered"),
        pytest.param("PyThon 3", "python 3", id="mixed-case-lowered"),
        pytest.param("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", id="ascii-alphabet"),
        pytest.param("0123456789 !@#$%^&*()_+-=[]{};:'\",.<>/?\\|", "0123456789 !@#$%^&*()_+-=[]{};:'\",.<>/?\\|", id="nonletters"),
        pytest.param(" \t\n\r", " \t\n\r", id="whitespace"),
        pytest.param("HELLO\nWorld\t!", "hello\nworld\t!", id="multiline"),
        pytest.param("ÉÀÖÑ", "éàöñ", id="accented-uppercase"),
        pytest.param("Straße", "straße", id="sharp-s-preserved"),
        pytest.param("İ", "i\u0307", id="unicode-length-expansion"),
        pytest.param("ΟΣ", "ος", id="contextual-greek-sigma"),
        pytest.param("中文 😀 123", "中文 😀 123", id="uncased-unicode"),
    ],
)
def test_current_implementation_lowercases_text(text, expected):
    assert invert_letter_case(text) == expected


def test_input_string_is_unchanged():
    text = "Hello WORLD"

    result = invert_letter_case(text)

    assert text == "Hello WORLD"
    assert result == "hello world"
