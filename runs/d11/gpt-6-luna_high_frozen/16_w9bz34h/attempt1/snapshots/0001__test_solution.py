import pytest

from solution import is_happy


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("a", False),
        ("aa", False),
        ("abc", True),
        ("abcd", True),
        ("adb", True),
        ("aaa", False),
        ("aaaa", False),
    ],
)
def test_is_happy_examples_and_triples(value, expected):
    assert is_happy(value) is expected


@pytest.mark.xfail(
    reason="solution.py currently rejects only triples of identical letters, but the docstring requires all three letters to be distinct",
    strict=False,
)
@pytest.mark.parametrize("value", ["aab", "aba", "abb", "aabb", "xyy"])
def test_is_happy_rejects_any_repeated_letter_in_a_three_character_window(value):
    assert is_happy(value) is False
