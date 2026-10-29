import pytest

from solution import longest


@pytest.mark.parametrize(
    ("strings", "expected"),
    [
        ([], None),
        (["a", "b", "c"], "a"),
        (["a", "bb", "ccc"], "ccc"),
        (["first longest", "short", "other longest"], "first longest"),
        (["short", "longer", "tiny"], "longer"),
        (["", "", "x"], "x"),
    ],
)
def test_longest(strings, expected):
    assert longest(strings) == expected


def test_longest_returns_first_string_when_maximum_length_is_tied():
    assert longest(["cat", "dog", "owl"]) == "cat"


def test_longest_returns_first_occurrence_when_tie_follows_a_shorter_string():
    assert longest(["a", "same", "long", "same"]) == "same"
