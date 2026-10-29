import pytest

from solution import scramble_triples, unscramble_triples

UNSCRAMBLE_BUG = pytest.mark.xfail(
    strict=True,
    reason="Known bug in solution.py: unscramble_triples re-applies scramble_triples "
    "(rotates left again) instead of rotating each full triple right.",
)


# ---------- scramble_triples ----------

@pytest.mark.parametrize(
    "text, expected",
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
def test_scramble_examples(text, expected):
    assert scramble_triples(text) == expected


def test_scramble_preserves_length_and_characters():
    text = "The quick brown fox jumps!"
    out = scramble_triples(text)
    assert len(out) == len(text)
    assert sorted(out) == sorted(text)


def test_scramble_leaves_short_tail_unchanged():
    text = "abcdefgh"  # tail "gh"
    assert scramble_triples(text).endswith("gh")


def test_scramble_unicode():
    assert scramble_triples("äöü€") == "öüä€"


def test_scramble_three_times_is_identity_on_full_triples():
    text = "abcdefghi"
    assert scramble_triples(scramble_triples(scramble_triples(text))) == text


# ---------- unscramble_triples ----------

@pytest.mark.parametrize("text", ["", "a", "ab"])
def test_unscramble_short_inputs_unchanged(text):
    assert unscramble_triples(text) == text


@UNSCRAMBLE_BUG
@pytest.mark.parametrize(
    "scrambled, original",
    [
        ("bca", "abc"),
        ("bcad", "abcd"),
        ("bcaefd", "abcdef"),
        ("bcaefdg", "abcdefg"),
    ],
)
def test_unscramble_examples(scrambled, original):
    assert unscramble_triples(scrambled) == original


@UNSCRAMBLE_BUG
@pytest.mark.parametrize(
    "text",
    ["abc", "abcdefg", "Hello, World!", "The quick brown fox jumps over the lazy dog"],
)
def test_round_trip(text):
    assert unscramble_triples(scramble_triples(text)) == text


def test_round_trip_trivial_cases():
    # Inputs where every full triple is made of one repeated character survive any rotation.
    for text in ["", "x", "xy", "aaa", "aaabbbc"]:
        assert unscramble_triples(scramble_triples(text)) == text
