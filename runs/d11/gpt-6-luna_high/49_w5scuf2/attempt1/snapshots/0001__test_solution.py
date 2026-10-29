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
        ("a a b b c", {"a": 2, "b": 2}),
        ("  a   b b  ", {"b": 2}),
        ("   ", {}),
    ],
)
def test_histogram(text, expected):
    assert histogram(text) == expected
