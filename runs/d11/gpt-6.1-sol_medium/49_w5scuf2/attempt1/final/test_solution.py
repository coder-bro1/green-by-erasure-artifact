import pytest

from solution import histogram


@pytest.mark.parametrize(
    ("letters", "expected"),
    [
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
        ("", {}),
        ("z", {"z": 1}),
        ("a a a a a", {"a": 5}),
        ("a b b c c c", {"c": 3}),
        ("c c c b b a", {"c": 3}),
        ("a b c a b c d", {"a": 2, "b": 2, "c": 2}),
        ("z a z b a z a c", {"z": 3, "a": 3}),
        (" ".join("abcdefghijklmnopqrstuvwxyz"), dict.fromkeys("abcdefghijklmnopqrstuvwxyz", 1)),
        (" ".join(["a"] * 100 + ["b"] * 99), {"a": 100}),
    ],
)
def test_histogram_returns_all_and_only_most_frequent_letters(letters, expected):
    assert histogram(letters) == expected


def test_histogram_calls_return_independent_dictionaries():
    first = histogram("a a b")
    first["a"] = 99
    first["z"] = 1

    assert histogram("a a b") == {"a": 2}
    assert histogram("b b a") == {"b": 2}
    assert histogram("") == {}
