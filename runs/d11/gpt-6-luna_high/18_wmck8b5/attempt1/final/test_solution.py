import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("source", "encoded"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "bca"),
        ("abcdef", "bcaefd"),
        ("abcdefgh", "bcaefdgh"),
        ("abcdefghi", "bcaefdhig"),
    ],
)
def test_encode_cyclic_rotates_each_complete_group(source, encoded):
    assert encode_cyclic(source) == encoded


@pytest.mark.parametrize(
    ("encoded", "decoded"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("bca", "abc"),
        ("bcaefd", "abcdef"),
        ("bcaefdgh", "abcdefgh"),
        ("bcaefdhig", "abcdefghi"),
    ],
)
def test_decode_cyclic_restores_source(encoded, decoded):
    assert decode_cyclic(encoded) == decoded


@pytest.mark.parametrize("source", ["", "x", "xy", "xyz", "abcdefgh", "a\U0001f642bc\u96ea"])
def test_decode_encode_round_trip(source):
    assert decode_cyclic(encode_cyclic(source)) == source
