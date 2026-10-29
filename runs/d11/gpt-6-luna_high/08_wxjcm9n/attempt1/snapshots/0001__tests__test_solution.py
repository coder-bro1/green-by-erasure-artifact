import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    ("s", "c", "expected"),
    [
        ("abcde", "ae", ("bcd", False)),
        ("abcdef", "b", ("acdef", False)),
        ("abcdedcba", "ab", ("cdedc", True)),
    ],
)
def test_documented_examples(s, c, expected):
    assert reverse_delete(s, c) == expected


def test_removes_every_occurrence_of_each_character():
    assert reverse_delete("banana", "an") == ("b", True)


def test_empty_removal_string_leaves_input_unchanged():
    assert reverse_delete("racecar", "") == ("racecar", True)


def test_removing_all_characters_returns_empty_palindrome():
    assert reverse_delete("abc", "cba") == ("", True)


def test_empty_input_returns_empty_palindrome():
    assert reverse_delete("", "abc") == ("", True)


def test_checks_palindrome_after_removal():
    assert reverse_delete("abccba", "b") == ("acca", True)
    assert reverse_delete("abccbd", "b") == ("accd", False)
