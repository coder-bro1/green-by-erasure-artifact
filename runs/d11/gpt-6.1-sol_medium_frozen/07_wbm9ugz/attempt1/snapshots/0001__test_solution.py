"""Tests for the current cyclic-string behavior in solution.py."""

import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("original", "expected"),
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
        ("1234567890", "2315648970"),
        ("a b\nc\t", " ba c\t\n"),
        ("বাংলা", "াংবলা"),
        ("🐍é中", "é中🐍"),
    ],
)
def test_encode_cyclic(original, expected):
    assert encode_cyclic(original) == expected


@pytest.mark.parametrize(
    ("encoded", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("bca", "cab"),
        ("bcad", "cabd"),
        ("bcade", "cabde"),
        ("bcaefd", "cabfde"),
        ("é中🐍", "中🐍é"),
    ],
)
def test_decode_cyclic_current_forward_rotation(encoded, expected):
    # The current decoder rotates left again rather than undoing encoding.
    assert decode_cyclic(encoded) == expected


@pytest.mark.parametrize("length", range(40))
def test_encoding_preserves_length_and_trailing_characters(length):
    original = "".join(chr(0x400 + index) for index in range(length))

    encoded = encode_cyclic(original)

    assert len(encoded) == len(original)
    remainder = length % 3
    if remainder:
        assert encoded[-remainder:] == original[-remainder:]


@pytest.mark.parametrize(
    "original", ["", "a", "ab", "abc", "abcde", "abcdefghi", "🐍é中\n !xy"]
)
def test_three_encodings_restore_original(original):
    assert encode_cyclic(encode_cyclic(encode_cyclic(original))) == original
