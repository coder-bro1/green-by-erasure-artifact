import pytest

from solution import is_happy


@pytest.mark.parametrize(
    "s, expected",
    [
        ("a", False),
        ("aa", False),
        ("abcd", True),
        ("aabb", False),
        ("adb", True),
        ("xyy", False),
    ],
)
def test_docstring_examples(s, expected):
    assert is_happy(s) is expected


@pytest.mark.parametrize("s", ["", "a", "ab", "xy"])
def test_shorter_than_three_is_not_happy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize(
    "s",
    [
        "abc",
        "abcabc",
        "iopaxpoi",
        "abcdefghijklmnopqrstuvwxyz",
        "xyzxyzxyz",
    ],
)
def test_happy_strings(s):
    assert is_happy(s) is True


@pytest.mark.parametrize(
    "s",
    [
        "aaa",         # all same
        "aab",         # first two equal
        "abb",         # last two equal
        "aba",         # first and third equal (non-adjacent)
        "abcb",        # violation in the last window only
        "abab",        # repeats with distance 2
        "iopaxioi",    # violation near the end
        "abcdeffgh",   # adjacent duplicate in the middle
    ],
)
def test_unhappy_strings(s):
    assert is_happy(s) is False


def test_violation_only_in_final_window():
    assert is_happy("abcdefgg") is False
    assert is_happy("abcdefgf") is False


def test_non_letter_characters():
    assert is_happy("123") is True
    assert is_happy("1 2") is True
    assert is_happy("  a") is False


def test_case_sensitive():
    assert is_happy("aAb") is True
    assert is_happy("aAa") is False
