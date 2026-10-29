import pytest

from solution import histogram


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", {}),
        ("a", {"a": 1}),
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
        ("z y z x y", {"z": 2, "y": 2}),
    ],
)
def test_histogram_returns_all_most_frequent_letters(text, expected):
    assert histogram(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "  a b b a  ",
        "a  b b  a",
        "\ta b b a\n",
    ],
)
def test_histogram_ignores_extra_whitespace(text):
    assert histogram(text) == {"a": 2, "b": 2}


def test_histogram_returns_empty_for_whitespace_only_input():
    assert histogram(" \t\n ") == {}
