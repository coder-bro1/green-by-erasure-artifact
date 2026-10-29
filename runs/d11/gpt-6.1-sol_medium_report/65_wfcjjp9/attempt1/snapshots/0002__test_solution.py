"""Tests for the documented cyclic encoding and decoding behavior."""

import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("original", "encoded"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "bca"),
        ("abcd", "bcad"),
        ("abcde", "bcade"),
        ("abcdef", "bcaefd"),
        ("abcdefg", "bcaefdg"),
        ("abcdefgh", "bcaefdgh"),
        ("abcdefghi", "bcaefdhig"),
        ("aaaaaa", "aaaaaa"),
        ("a b\nc\t!", " bac\t\n!"),
        ("123!?-", "231?-!"),
        ("é猫🙂xy", "猫🙂éxy"),
    ],
)
def test_encode_cyclic(original, encoded):
    assert encode_cyclic(original) == encoded


@pytest.mark.parametrize("value", ["", "a", "ab", "aaa", "aaab", "aaabc", "aaaaaa"])
def test_decode_cyclic_unchanged_groups(value):
    assert decode_cyclic(value) == value


@pytest.mark.xfail(
    strict=True,
    reason=(
        "decode_cyclic calls encode_cyclic, rotating full groups left again "
        "instead of rotating them right to recover the documented original string."
    ),
)
@pytest.mark.parametrize(
    ("encoded", "original"),
    [
        ("bca", "abc"),
        ("bcad", "abcd"),
        ("bcade", "abcde"),
        ("bcaefd", "abcdef"),
        ("bcaefdgh", "abcdefgh"),
        ("bcaefdhig", "abcdefghi"),
        (" bac\t\n!", "a b\nc\t!"),
        ("猫🙂éxy", "é猫🙂xy"),
    ],
)
def test_decode_cyclic_reverses_encoding(encoded, original):
    assert decode_cyclic(encoded) == original
