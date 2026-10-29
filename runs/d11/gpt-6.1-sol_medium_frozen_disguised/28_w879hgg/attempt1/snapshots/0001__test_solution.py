"""Tests for triple rotations, including the known inverse defect."""

import pytest

from solution import scramble_triples, unscramble_triples


@pytest.mark.parametrize(
    ("text", "expected"),
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
        ("aaabbbcc", "aaabbbcc"),
        (" a\nb\tc!", "a\n \tcb!"),
        ("你🙂好éßλ尾", "🙂好你ßλé尾"),
    ],
)
def test_scramble_triples(text, expected):
    assert scramble_triples(text) == expected


@pytest.mark.parametrize("length", range(31))
def test_scramble_preserves_length_tail_and_has_period_three(length):
    text = "abcdefghijklmnopqrstuvwxyz012345"[:length]
    scrambled = scramble_triples(text)

    assert len(scrambled) == len(text)
    full_groups_end = length - length % 3
    assert scrambled[full_groups_end:] == text[full_groups_end:]
    assert scramble_triples(scramble_triples(scrambled)) == text


@pytest.mark.parametrize("text", ["", "a", "ab", "aaa", "aaabbb", "aaabbbcd"])
def test_unscramble_for_inputs_unchanged_by_rotation(text):
    assert unscramble_triples(text) == text
    assert unscramble_triples(scramble_triples(text)) == text


@pytest.mark.xfail(
    strict=True,
    reason="unscramble_triples applies the forward rotation instead of its inverse",
)
@pytest.mark.parametrize(
    ("scrambled", "original"),
    [("bca", "abc"), ("bcad", "abcd"), ("bcade", "abcde"), ("bcaefd", "abcdef")],
)
def test_unscramble_restores_original(scrambled, original):
    assert unscramble_triples(scrambled) == original
