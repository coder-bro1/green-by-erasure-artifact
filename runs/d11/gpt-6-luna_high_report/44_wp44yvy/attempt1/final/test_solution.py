import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    ("source", "characters_to_delete", "expected"),
    [
        # Examples from the function's docstring.
        ("abcde", "ae", ("bcd", False)),
        ("abcdef", "b", ("acdef", False)),
        ("abcdedcba", "ab", ("cdedc", True)),
        # Deleting every occurrence, including repeated characters.
        ("banana", "an", ("b", True)),
        # Empty deletion sets preserve the input.
        ("racecar", "", ("racecar", True)),
        ("hello", "", ("hello", False)),
        # Removing all characters yields the empty palindrome.
        ("xyz", "zyx", ("", True)),
        # Deletion is case-sensitive and preserves the order of survivors.
        ("aAba", "a", ("Ab", False)),
        # The empty source is itself a palindrome.
        ("", "anything", ("", True)),
    ],
)
def test_reverse_delete(source, characters_to_delete, expected):
    assert reverse_delete(source, characters_to_delete) == expected
