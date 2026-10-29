import pytest
from solution import first_longest


def test_empty_list_returns_none():
    assert first_longest([]) is None


@pytest.mark.parametrize("words, expected", [
    (["xy", "abc", "q"], "abc"),
    (["no", "at"], "no"),
    (["a"], "a"),
    ([""], ""),
    (["", "", ""], ""),
    (["a", "bb", "cc", "d"], "bb"),
    (["abc", "de", "fgh"], "abc"),
    (["short", "longer", "longest"], "longest"),
    (["x", "", "y"], "x"),
])
def test_first_longest(words, expected):
    assert first_longest(words) == expected


def test_returns_earliest_object_on_tie():
    a, b = "same", "same"
    words = [a, "xy", b]
    assert first_longest(words) is words[0]


def test_does_not_mutate_input():
    words = ["b", "aaa", "cc"]
    first_longest(words)
    assert words == ["b", "aaa", "cc"]
