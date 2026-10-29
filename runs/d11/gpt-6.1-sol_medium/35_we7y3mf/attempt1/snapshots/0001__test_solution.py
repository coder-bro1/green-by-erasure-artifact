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
        ("abcdefgh", "bcaefdgh"),
        ("abcdefghi", "bcaefdhig"),
        ("aaaaaa", "aaaaaa"),
        ("a b\nc!", " ba c!\n"),
        ("αβγ🙂🙃😉終", "βγα🙃😉🙂終"),
    ],
)
def test_encode_cyclic(original, encoded):
    assert encode_cyclic(original) == encoded


@pytest.mark.parametrize(
    ("encoded", "decoded"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("bca", "abc"),
        ("bcad", "abcd"),
        ("bcade", "abcde"),
        ("bcaefd", "abcdef"),
        ("bcaefdgh", "abcdefgh"),
        ("bcaefdhig", "abcdefghi"),
        ("βγα🙃😉🙂終", "αβγ🙂🙃😉終"),
    ],
)
def test_decode_cyclic(encoded, decoded):
    assert decode_cyclic(encoded) == decoded


@pytest.mark.parametrize("length", range(31))
def test_round_trip_preserves_string(length):
    original = "abcdefghijklmnopqrstuvwxyz012345"[:length]

    assert decode_cyclic(encode_cyclic(original)) == original
    assert encode_cyclic(decode_cyclic(original)) == original
