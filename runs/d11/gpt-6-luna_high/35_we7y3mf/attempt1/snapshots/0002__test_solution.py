import pytest

from solution import decode_cyclic, encode_cyclic


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "bca"),
        ("abcdef", "bcaefd"),
        ("abcdefgh", "bcaefdgh"),
        ("a🙂c漢", "🙂ca漢"),
    ],
)
def test_encode_cyclic_rotates_each_complete_group(source, expected):
    assert encode_cyclic(source) == expected


@pytest.mark.parametrize(
    ("encoded", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("bca", "abc"),
        ("bcaefd", "abcdef"),
        ("bcaefdgh", "abcdefgh"),
        ("🙂ca漢", "a🙂c漢"),
    ],
)
def test_decode_cyclic_restores_source(encoded, expected):
    assert decode_cyclic(encoded) == expected


@pytest.mark.parametrize("source", ["", "x", "xy", "xyz", "abcdefgh", "a🙂c漢"])
def test_decode_is_inverse_of_encode(source):
    assert decode_cyclic(encode_cyclic(source)) == source
