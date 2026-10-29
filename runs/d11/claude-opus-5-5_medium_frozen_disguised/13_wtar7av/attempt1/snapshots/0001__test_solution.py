import pytest
from solution import strip_and_mirror_check


@pytest.mark.parametrize("text, banned, expected", [
    ("racecar", "x", ("racecar", True)),
    ("banana", "b", ("anana", True)),
    ("level", "v", ("leel", True)),
])
def test_docstring_examples(text, banned, expected):
    assert strip_and_mirror_check(text, banned) == expected


def test_non_palindrome_after_strip():
    assert strip_and_mirror_check("hello", "x") == ("hello", False)


def test_stripping_creates_palindrome():
    assert strip_and_mirror_check("abxba", "x") == ("abba", True)


def test_stripping_breaks_palindrome():
    assert strip_and_mirror_check("abcba", "a") == ("bcb", True)
    assert strip_and_mirror_check("abca", "c") == ("aba", True)
    assert strip_and_mirror_check("aba", "b") == ("aa", True)
    assert strip_and_mirror_check("abcxba", "") == ("abcxba", False)


def test_removes_all_occurrences_of_every_banned_char():
    result, _ = strip_and_mirror_check("a1b2c3a", "123")
    assert result == "abca"


def test_empty_banned_leaves_text_unchanged():
    assert strip_and_mirror_check("abc", "") == ("abc", False)


def test_empty_text():
    assert strip_and_mirror_check("", "abc") == ("", True)


def test_everything_banned_gives_empty_palindrome():
    assert strip_and_mirror_check("abc", "cba") == ("", True)


def test_single_character_is_palindrome():
    assert strip_and_mirror_check("z", "") == ("z", True)


def test_case_sensitive():
    assert strip_and_mirror_check("Aba", "") == ("Aba", False)
    assert strip_and_mirror_check("AbA", "a") == ("AbA", True)


def test_banned_can_be_list_or_set():
    assert strip_and_mirror_check("racecar", {"e"}) == ("raccar", True)
    assert strip_and_mirror_check("racecar", ["r"]) == ("aceca", True)


def test_return_types():
    result = strip_and_mirror_check("ab", "")
    assert isinstance(result, tuple) and len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], bool)
