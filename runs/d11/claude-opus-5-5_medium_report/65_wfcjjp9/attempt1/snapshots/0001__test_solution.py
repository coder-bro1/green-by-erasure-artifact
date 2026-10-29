import pytest

from solution import decode_cyclic, encode_cyclic

DECODE_BUG = (
    "decode_cyclic just calls encode_cyclic, which rotates each full 3-char group "
    "left a second time instead of rotating it back right, so it does not invert "
    "encode_cyclic (e.g. 'abc' -> 'bca' -> 'cab')"
)


# ---------- encode_cyclic ----------

@pytest.mark.parametrize(
    "s, expected",
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("abc", "bca"),
        ("abcd", "bcad"),
        ("abcde", "bcade"),
        ("abcdef", "bcaefd"),
        ("abcdefg", "bcaefdg"),
        ("aaa", "aaa"),
        ("a b", " ba"),
    ],
)
def test_encode_cyclic(s, expected):
    assert encode_cyclic(s) == expected


def test_encode_preserves_length_and_characters():
    s = "the quick brown fox jumps"
    out = encode_cyclic(s)
    assert len(out) == len(s)
    assert sorted(out) == sorted(s)


def test_encode_three_times_is_identity():
    s = "abcdefghijk"
    assert encode_cyclic(encode_cyclic(encode_cyclic(s))) == s


# ---------- decode_cyclic: cases that work ----------

@pytest.mark.parametrize("s", ["", "a", "ab", "aaa", "aaabbb", "zzzzzzz"])
def test_decode_roundtrip_trivial_cases(s):
    # Strings shorter than 3 and groups of identical chars are unaffected by rotation.
    assert decode_cyclic(encode_cyclic(s)) == s


# ---------- decode_cyclic: cases exposing the bug ----------

@pytest.mark.xfail(strict=True, reason=DECODE_BUG)
@pytest.mark.parametrize(
    "encoded, expected",
    [
        ("bca", "abc"),
        ("bcad", "abcd"),
        ("bcaefd", "abcdef"),
        ("bcaefdg", "abcdefg"),
    ],
)
def test_decode_cyclic_known_values(encoded, expected):
    assert decode_cyclic(encoded) == expected


@pytest.mark.xfail(strict=True, reason=DECODE_BUG)
@pytest.mark.parametrize("s", ["abc", "hello world", "abcdefghij", "pytest!"])
def test_decode_roundtrip(s):
    assert decode_cyclic(encode_cyclic(s)) == s
