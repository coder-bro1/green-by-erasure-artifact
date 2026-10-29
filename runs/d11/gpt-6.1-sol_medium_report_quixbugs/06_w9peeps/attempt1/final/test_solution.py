"""Tests for the documented longest-common-subsequence contract."""

from itertools import combinations, product

import pytest

from solution import longest_common_subsequence


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("", "", ""),
        ("", "abc", ""),
        ("abc", "", ""),
        ("a", "a", "a"),
        ("a", "b", ""),
        ("abc", "XYZ", ""),
        ("abc", "abc", "abc"),
        ("abc", "aXbYc", "abc"),
        ("aXbYc", "abc", "abc"),
        ("headache", "pentadactyl", "eadac"),
        ("aaaa", "aa", "aa"),
        ("aa", "aaaa", "aa"),
        ("banana", "ananas", "anana"),
        ("ABC", "abc", ""),
        ("a b!", "aX bY!", "a b!"),
        ("é猫🙂", "XéY猫Z🙂", "é猫🙂"),
    ],
)
def test_unique_longest_common_subsequence(a, b, expected):
    assert longest_common_subsequence(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "valid_results"),
    [
        ("ab", "ba", {"a", "b"}),
        ("abc", "bac", {"ac", "bc"}),
        ("ABCBDAB", "BDCABA", {"BCAB", "BCBA", "BDAB"}),
    ],
)
def test_any_longest_result_is_allowed_when_lengths_tie(a, b, valid_results):
    assert longest_common_subsequence(a, b) in valid_results


def _subsequences(value):
    """Enumerate subsequences independently of the implementation's recursion."""
    return {
        "".join(value[index] for index in indices)
        for length in range(len(value) + 1)
        for indices in combinations(range(len(value)), length)
    }


_SHORT_STRINGS = [
    "".join(letters)
    for length in range(5)
    for letters in product("ab", repeat=length)
]
_SHORT_SUBSEQUENCES = {value: _subsequences(value) for value in _SHORT_STRINGS}


@pytest.mark.parametrize("a", _SHORT_STRINGS)
@pytest.mark.parametrize("b", _SHORT_STRINGS)
def test_all_short_binary_strings_against_exhaustive_oracle(a, b):
    common = _SHORT_SUBSEQUENCES[a] & _SHORT_SUBSEQUENCES[b]
    result = longest_common_subsequence(a, b)

    assert isinstance(result, str)
    assert result in common, "Result must preserve character order in both inputs"
    assert len(result) == max(map(len, common)), "Result must have maximal length"
