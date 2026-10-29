import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("Hello", "hELLO"),
        ("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),
        ("PyThOn", "pYtHoN"),
        ("Hello, World! 123", "hELLO, wORLD! 123"),
        ("123 !@#$%^&*()_+-=[]{};:,.?", "123 !@#$%^&*()_+-=[]{};:,.?"),
        (" \t\n\r", " \t\n\r"),
        ("A\tB\nc\rd", "a\tb\nC\rD"),
        ("École Über Ångström", "éCOLE üBER åNGSTRÖM"),
        ("ΑβΓ ПрИвЕт", "αΒγ пРиВеТ"),
        ("你好 🙂", "你好 🙂"),
        ("Straße", "sTRASSE"),
    ],
)
def test_flip_case(text, expected):
    assert flip_case(text) == expected
