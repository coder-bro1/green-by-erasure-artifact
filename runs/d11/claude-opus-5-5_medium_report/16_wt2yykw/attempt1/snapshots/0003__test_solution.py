import random
import string

import pytest

from solution import encode_cyclic, decode_cyclic


@pytest.mark.parametrize(
    "plain, encoded",
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
        ("123456789", "231564897"),
    ],
)
def test_encode_known_values(plain, encoded):
    assert encode_cyclic(plain) == encoded


@pytest.mark.parametrize(
    "encoded, plain",
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ab"),
        ("bca", "abc"),
        ("bcad", "abcd"),
        ("bcaefdg", "abcdefg"),
    ],
)
def test_decode_known_values(encoded, plain):
    assert decode_cyclic(encoded) == plain


def test_encode_preserves_length_and_characters():
    s = "hello world!"
    out = encode_cyclic(s)
    assert len(out) == len(s)
    assert sorted(out) == sorted(s)


def test_encode_handles_unicode_and_whitespace():
    s = "äöü ß
"
    assert encode_cyclic(s) == "öüäß
 "
    assert decode_cyclic(encode_cyclic(s)) == s


def test_round_trip_random():
    rng = random.Random(1234)
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    for _ in range(200):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 50)))
        assert decode_cyclic(encode_cyclic(s)) == s


@pytest.mark.parametrize("n", range(0, 12))
def test_round_trip_all_lengths(n):
    s = "".join(chr(ord("a") + i) for i in range(n))
    assert decode_cyclic(encode_cyclic(s)) == s


def test_encode_changes_full_groups_of_distinct_chars():
    assert encode_cyclic("xyz") != "xyz"


def test_returns_str():
    assert isinstance(encode_cyclic("abcd"), str)
    assert isinstance(decode_cyclic("abcd"), str)
