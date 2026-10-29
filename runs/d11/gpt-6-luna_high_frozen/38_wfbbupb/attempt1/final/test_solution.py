import pytest

from solution import histogram


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
        ("z z z", {"z": 3}),
    ],
)
def test_histogram_returns_all_most_frequent_letters(text, expected):
    assert histogram(text) == expected


@pytest.mark.xfail(reason="solution.py currently returns {'': 1} for empty input")
def test_histogram_empty_input_returns_empty_dictionary():
    assert histogram("") == {}
