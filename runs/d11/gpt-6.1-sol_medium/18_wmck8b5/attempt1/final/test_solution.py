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
        ("abcdefghi", "bcaefdhig"),
        ("abcdefghijk", "bcaefdhigjk"),
        ("aaaaaa", "aaaaaa"),
        ("a b\nc\t!", " bac\t\n!"),
        ("é猫🙂Ωλ", "猫🙂éΩλ"),
    ],
)
def test_encode_cyclic_known_outputs(original, encoded):
    assert encode_cyclic(original) == encoded


@pytest.mark.parametrize(
    ("encoded", "decoded"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "cab"),
        ("abcd", "cabd"),
        ("abcde", "cabde"),
        ("abcdef", "cabfde"),
        ("abcdefghi", "cabfdeigh"),
        ("猫🙂éΩλ", "é猫🙂Ωλ"),
    ],
)
def test_decode_cyclic_known_outputs(encoded, decoded):
    assert decode_cyclic(encoded) == decoded


@pytest.mark.parametrize("length", range(31))
def test_round_trip_and_rotation_properties(length):
    original = "abcdefghijklmnopqrstuvwxyz0123"[:length]
    encoded = encode_cyclic(original)

    assert decode_cyclic(encoded) == original
    assert encode_cyclic(decode_cyclic(original)) == original
    assert encode_cyclic(encode_cyclic(encoded)) == original
    assert len(encoded) == len(original)

    remainder = length % 3
    if remainder:
        assert encoded[-remainder:] == original[-remainder:]
