import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "bca"),
        ("abcd", "bcad"),
        ("abcdef", "bcaefd"),
        ("abcdefg", "bcaefd g".replace(" ", "")),
        ("a b!", "b !a"),
    ],
)
def test_encode_cyclic(text, expected):
    assert encode_cyclic(text) == expected


@pytest.mark.parametrize(
    ("encoded", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("bca", "abc"),
        ("bcad", "abcd"),
        ("bcaefd", "abcdef"),
        ("bcaefdg", "abcdefg"),
        ("b !a", "a b!"),
    ],
)
def test_decode_cyclic(encoded, expected):
    assert decode_cyclic(encoded) == expected


@pytest.mark.parametrize("text", ["", "x", "xy", "xyz", "abcdefghijk"])
def test_decode_reverses_encode(text):
    assert decode_cyclic(encode_cyclic(text)) == text
