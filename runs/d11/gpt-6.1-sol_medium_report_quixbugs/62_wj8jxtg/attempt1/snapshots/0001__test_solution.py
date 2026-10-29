import pytest

from solution import longest_common_subsequence


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("", "", {""}),
        ("", "abc", {""}),
        ("abc", "", {""}),
        ("abc", "xyz", {""}),
        ("a", "a", {"a"}),
        ("abc", "abc", {"abc"}),
        ("abc", "axbxc", {"abc"}),
        ("axbxc", "abc", {"abc"}),
        ("abc", "cba", {"a", "b", "c"}),
        ("ab", "ba", {"a", "b"}),
        ("abc", "bac", {"ac", "bc"}),
        ("ABC", "abc", {""}),
        ("headache", "pentadactyl", {"eadac"}),
    ],
)
def test_longest_common_subsequence(a, b, expected):
    # The contract permits any longest result when there is a tie.
    result = longest_common_subsequence(a, b)
    assert isinstance(result, str)
    assert result in expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("aa", "a", "a"),
        ("aaaa", "aa", "aa"),
        ("aab", "ab", "ab"),
        ("banana", "ban", "ban"),
    ],
)
def test_matching_characters_must_consume_both_inputs(a, b, expected):
    assert longest_common_subsequence(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [("a", "aa", "a"), ("aa", "aaaa", "aa"), ("ab", "aab", "ab")],
)
def test_extra_repeated_characters_in_second_input(a, b, expected):
    assert longest_common_subsequence(a, b) == expected
