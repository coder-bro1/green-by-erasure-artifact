"""Tests for cycling three-character groups and reversing the encoding."""

import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("original", "encoded"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("a", "a", id="one-character"),
        pytest.param("ab", "ab", id="two-characters"),
        pytest.param("abc", "bca", id="one-full-group"),
        pytest.param("abcd", "bcad", id="one-character-remainder"),
        pytest.param("abcde", "bcade", id="two-character-remainder"),
        pytest.param("abcdef", "bcaefd", id="two-full-groups"),
        pytest.param("abcdefgh", "bcaefdgh", id="multiple-groups-with-remainder"),
        pytest.param("abcdefghi", "bcaefdhig", id="three-full-groups"),
        pytest.param("aaaaaaa", "aaaaaaa", id="repeated-characters"),
        pytest.param("a b\nc!", " bac!\n", id="whitespace-and-punctuation"),
        pytest.param("αβγ🙂中éZ", "βγα中é🙂Z", id="unicode"),
    ],
)
def test_encode_cyclic(original, encoded):
    assert encode_cyclic(original) == encoded


@pytest.mark.parametrize(
    ("encoded", "decoded"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("a", "a", id="one-character"),
        pytest.param("ab", "ab", id="two-characters"),
        pytest.param("bca", "abc", id="one-full-group"),
        pytest.param("bcad", "abcd", id="one-character-remainder"),
        pytest.param("bcade", "abcde", id="two-character-remainder"),
        pytest.param("bcaefd", "abcdef", id="two-full-groups"),
        pytest.param("bcaefdgh", "abcdefgh", id="multiple-groups-with-remainder"),
        pytest.param("bcaefdhig", "abcdefghi", id="three-full-groups"),
        pytest.param(" bac!\n", "a b\nc!", id="whitespace-and-punctuation"),
        pytest.param("βγα中é🙂Z", "αβγ🙂中éZ", id="unicode"),
    ],
)
def test_decode_cyclic(encoded, decoded):
    assert decode_cyclic(encoded) == decoded


@pytest.mark.parametrize("length", range(31))
def test_round_trip_across_group_boundaries(length):
    original = "abcdefghijklmnopqrstuvwxyz0123"[:length]
    assert decode_cyclic(encode_cyclic(original)) == original
    assert encode_cyclic(decode_cyclic(original)) == original
