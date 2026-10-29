import random
import string

import pytest

from solution import decode_cyclic, encode_cyclic


def _reference_decode(s: str) -> str:
    """Correct inverse of encode_cyclic: rotate each full group of 3 right by one."""
    groups = [s[i:i + 3] for i in range(0, len(s), 3)]
    return "".join(g[-1] + g[:-1] if len(g) == 3 else g for g in groups)


# ---------------------------------------------------------------- encode_cyclic

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
        ("a b", " ba"),
    ],
)
def test_encode_known_values(plain, encoded):
    assert encode_cyclic(plain) == encoded


def test_encode_preserves_length_and_characters():
    rng = random.Random(0)
    for _ in range(200):
        s = "".join(rng.choices(string.printable, k=rng.randint(0, 40)))
        out = encode_cyclic(s)
        assert len(out) == len(s)
        assert sorted(out) == sorted(s)


def test_encode_leaves_trailing_partial_group_untouched():
    for tail in ("x", "xy"):
        s = "abcdef" + tail
        assert encode_cyclic(s).endswith(tail)


def test_encode_unicode():
    assert encode_cyclic("äöü€") == "öüä€"


def test_encode_three_times_is_identity():
    rng = random.Random(1)
    for _ in range(200):
        s = "".join(rng.choices(string.ascii_letters, k=rng.randint(0, 30)))
        assert encode_cyclic(encode_cyclic(encode_cyclic(s))) == s


def test_encode_does_not_mutate_or_return_non_str():
    s = "hello world"
    out = encode_cyclic(s)
    assert isinstance(out, str)
    assert s == "hello world"


# ---------------------------------------------------------------- decode_cyclic

@pytest.mark.parametrize("s", ["", "a", "ab"])
def test_decode_short_strings_unchanged(s):
    assert decode_cyclic(s) == s


@pytest.mark.parametrize("s", ["", "a", "ab", "aaa", "zzzzzz"])
def test_roundtrip_trivial_cases(s):
    # Strings shorter than 3 or made of identical chars survive regardless.
    assert decode_cyclic(encode_cyclic(s)) == s


def test_decode_current_behaviour_matches_encode():
    # Documents the implementation as written: decode_cyclic delegates to encode_cyclic.
    for s in ["abc", "abcdef", "hello world"]:
        assert decode_cyclic(s) == encode_cyclic(s)


def test_reference_decode_is_correct_inverse():
    # Sanity-check the helper used by the xfail tests below.
    rng = random.Random(2)
    for _ in range(200):
        s = "".join(rng.choices(string.ascii_letters, k=rng.randint(0, 30)))
        assert _reference_decode(encode_cyclic(s)) == s


@pytest.mark.xfail(
    strict=True,
    reason="BUG: decode_cyclic calls encode_cyclic once; it must rotate right "
    "(i.e. apply encode_cyclic twice) to invert encoding.",
)
def test_decode_inverts_encode_known_value():
    assert decode_cyclic("bca") == "abc"


@pytest.mark.xfail(strict=True, reason="BUG: decode_cyclic is not the inverse of encode_cyclic.")
def test_roundtrip_random():
    rng = random.Random(3)
    for _ in range(100):
        s = "".join(rng.choices(string.ascii_lowercase, k=rng.randint(3, 30)))
        assert decode_cyclic(encode_cyclic(s)) == s
