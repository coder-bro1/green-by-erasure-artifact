import pytest
import sys
from pathlib import Path

# Keep the repository root importable when pytest is invoked via its console
# script, which does not always place the current directory on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solution import is_happy


@pytest.mark.parametrize("value", ["", "a", "ab"])
def test_strings_shorter_than_three_are_not_happy(value):
    assert is_happy(value) is False


@pytest.mark.parametrize("value", ["abc", "abcd", "adb", "abcab"])
def test_strings_with_distinct_characters_in_every_three_character_window(value):
    assert is_happy(value) is True


@pytest.mark.parametrize(
    "value",
    [
        "aaa",  # first and second positions match
        "aab",  # first and second positions match
        "abb",  # second and third positions match
        "aba",  # first and third positions match
        "aabb",  # a duplicate occurs in at least one window
        "abcaad",  # duplicate occurs in a later window
    ],
)
def test_any_repeated_character_in_a_three_character_window_is_not_happy(value):
    assert is_happy(value) is False


def test_characters_may_repeat_when_they_are_not_in_the_same_window():
    assert is_happy("abca") is True


def test_non_letter_characters_are_compared_as_characters():
    assert is_happy("a1!") is True
    assert is_happy("a1a") is False
