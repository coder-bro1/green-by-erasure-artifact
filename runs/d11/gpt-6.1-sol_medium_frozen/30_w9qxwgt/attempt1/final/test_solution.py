"""Characterize the current implementation, which lowercases rather than swaps case."""

import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("ABCXYZ", "abcxyz", id="uppercase-ascii"),
        pytest.param("abcxyz", "abcxyz", id="lowercase-ascii"),
        pytest.param("Hello", "hello", id="documented-example-current-behavior"),
        pytest.param("aBcDeF", "abcdef", id="alternating-case"),
        pytest.param("1234567890", "1234567890", id="digits"),
        pytest.param("!?.,-_()[]{}", "!?.,-_()[]{}", id="punctuation"),
        pytest.param(" \t\n\r", " \t\n\r", id="whitespace"),
        pytest.param("Hello, WORLD! 123", "hello, world! 123", id="mixed-content"),
        pytest.param("ONE\nTwo\tTHREE", "one\ntwo\tthree", id="multiline"),
        pytest.param("ÀÉÖÑ", "àéöñ", id="accented-latin"),
        pytest.param("Σ", "σ", id="greek-letter"),
        pytest.param("ΟΣ", "ος", id="contextual-final-sigma"),
        pytest.param("ПРИВЕТ", "привет", id="cyrillic"),
        pytest.param("İ", "i\u0307", id="unicode-length-expansion"),
        pytest.param("Straße ẞ", "straße ß", id="german-sharp-s"),
        pytest.param("中文 😀", "中文 😀", id="uncased-unicode"),
        pytest.param("A\x00B", "a\x00b", id="embedded-null"),
        pytest.param("ABC" * 1000, "abc" * 1000, id="long-string"),
    ],
)
def test_flip_case_current_lowercasing_behavior(text, expected):
    assert flip_case(text) == expected


def test_flip_case_returns_a_string():
    assert isinstance(flip_case("Hello"), str)


def test_flip_case_does_not_change_input():
    text = "Hello, WORLD!"
    flip_case(text)
    assert text == "Hello, WORLD!"


def test_flip_case_can_be_called_repeatedly():
    assert flip_case("FIRST") == "first"
    assert flip_case("SECOND") == "second"
    assert flip_case("FIRST") == "first"
