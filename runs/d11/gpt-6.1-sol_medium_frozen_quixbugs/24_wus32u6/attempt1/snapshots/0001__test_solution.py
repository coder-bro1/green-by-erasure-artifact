"""Behavior tests and known-defect regressions for longest_common_subsequence."""

from itertools import permutations

import pytest

from solution import longest_common_subsequence


def is_subsequence(candidate, source):
    remaining = iter(source)
    return all(character in remaining for character in candidate)


def lcs_length(a, b):
    """Independent dynamic-programming oracle; ties do not require a fixed string."""
    previous = [0] * (len(b) + 1)
    for left in a:
        current = [0]
        for column, right in enumerate(b, start=1):
            if left == right:
                current.append(previous[column - 1] + 1)
            else:
                current.append(max(previous[column], current[-1]))
        previous = current
    return previous[-1]


def assert_valid_lcs(a, b):
    result = longest_common_subsequence(a, b)
    assert isinstance(result, str)
    assert is_subsequence(result, a), (a, b, result)
    assert is_subsequence(result, b), (a, b, result)
    assert len(result) == lcs_length(a, b), (a, b, result)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        ("", "", ""),
        ("", "abc", ""),
        ("abc", "", ""),
        ("a", "a", "a"),
        ("a", "b", ""),
        ("abc", "XYZ", ""),
        ("abc", "abc", "abc"),
        ("ace", "abcde", "ace"),
        ("abcde", "ace", "ace"),
        ("a", "aaaa", "a"),
        ("abc", "aabbcc", "abc"),
        ("AbC", "abc", "b"),
        ("a b", "ab", "ab"),
        ("a\nb", "x\ny", "\n"),
        ("é猫🙂", "xéy猫z🙂", "é猫🙂"),
    ],
)
def test_unique_longest_common_subsequence(a, b, expected):
    assert longest_common_subsequence(a, b) == expected
    assert_valid_lcs(a, b)


@pytest.mark.parametrize("a,b", [("ab", "ba"), ("abc", "bac"), ("abcd", "badc")])
def test_equal_length_answers_may_choose_either_subsequence(a, b):
    assert_valid_lcs(a, b)


def test_all_short_strings_with_distinct_characters():
    strings = [
        "".join(characters)
        for length in range(4)
        for characters in permutations("abc", length)
    ]
    for a in strings:
        for b in strings:
            assert_valid_lcs(a, b)


@pytest.mark.xfail(
    strict=True,
    reason="Matched characters advance only a, allowing reuse of a character in b.",
)
@pytest.mark.parametrize("a,b", [("aa", "a"), ("aaaa", "aa"), ("abba", "aba"), ("banana", "ana")])
def test_matching_characters_cannot_be_reused(a, b):
    assert_valid_lcs(a, b)
