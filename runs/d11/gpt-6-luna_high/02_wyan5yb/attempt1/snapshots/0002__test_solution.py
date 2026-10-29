import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    ("s", "c", "expected"),
    [
        ("abcde", "ae", ("bcd", False)),
        ("abcdef", "b", ("acdef", False)),
        ("abcdedcba", "ab", ("cdedc", True)),
    ],
)
def test_documented_examples(s, c, expected):
    assert reverse_delete(s, c) == expected


@pytest.mark.parametrize(
    ("s", "c", "expected"),
    [
        ("", "abc", ("", True)),
        ("abba", "xyz", ("abba", True)),
        ("abc", "abc", ("", True)),
        ("aabb", "a", ("bb", True)),
        ("Aa", "a", ("A", True)),
        ("abca", "aab", ("c", True)),
    ],
)
def test_deletion_and_palindrome_edge_cases(s, c, expected):
    assert reverse_delete(s, c) == expected
