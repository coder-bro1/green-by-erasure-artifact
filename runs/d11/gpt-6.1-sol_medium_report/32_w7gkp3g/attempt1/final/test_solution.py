import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("Hello", "hELLO", id="docstring-example"),
        pytest.param("", "", id="empty-string"),
        pytest.param("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", id="lowercase"),
        pytest.param("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", id="uppercase"),
        pytest.param("aBcDeF", "AbCdEf", id="mixed-case"),
        pytest.param("Hello, World! 123", "hELLO, wORLD! 123", id="sentence"),
        pytest.param("0123456789!?.,_-+", "0123456789!?.,_-+", id="uncased-symbols"),
        pytest.param(" \t\n\r", " \t\n\r", id="whitespace"),
        pytest.param(" A\tb\nC\r ", " a\tB\nc\r ", id="preserve-whitespace"),
        pytest.param("\u00e9\u00c9\u00e4\u00c4", "\u00c9\u00e9\u00c4\u00e4", id="accented-letters"),
        pytest.param("\u03b1\u0392\u03b3", "\u0391\u03b2\u0393", id="greek-letters"),
        pytest.param("\u0430\u0411\u0432", "\u0410\u0431\u0412", id="cyrillic-letters"),
        pytest.param("\u4e2d\u6587\U0001f642", "\u4e2d\u6587\U0001f642", id="uncased-unicode"),
        pytest.param("a\x00B", "A\x00b", id="embedded-null"),
    ],
)
def test_flip_case(text, expected):
    assert flip_case(text) == expected


def test_flip_case_long_string():
    text = "aB 123!\n" * 10_000
    expected = "Ab 123!\n" * 10_000

    assert flip_case(text) == expected
