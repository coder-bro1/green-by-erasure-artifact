import pytest

from solution import flip_case


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("Hello", "hELLO", id="docstring-example"),
        pytest.param("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", id="lowercase"),
        pytest.param("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", id="uppercase"),
        pytest.param("PyThOn", "pYtHoN", id="mixed-case"),
        pytest.param("", "", id="empty"),
        pytest.param("123 !?.,_-", "123 !?.,_-", id="nonletters"),
        pytest.param("Hello, World! 123", "hELLO, wORLD! 123", id="letters-and-nonletters"),
        pytest.param("A b\tC\nd\r\n", "a B\tc\nD\r\n", id="whitespace"),
        pytest.param("ÄÖÜäöü Éé Ωω", "äöüÄÖÜ éÉ ωΩ", id="unicode-case"),
        pytest.param("你好 🎉", "你好 🎉", id="uncased-unicode"),
    ],
)
def test_flip_case(text, expected):
    assert flip_case(text) == expected
