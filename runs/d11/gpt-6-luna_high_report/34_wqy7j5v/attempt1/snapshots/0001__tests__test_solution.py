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
        ("c a b c a c", {"c": 3}),
        ("z z a a b", {"z": 2, "a": 2}),
    ],
)
def test_histogram_returns_all_most_frequent_letters(text, expected):
    assert histogram(text) == expected
