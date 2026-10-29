"""Tests for the documented space-separated lowercase-letter histogram."""

import pytest

from solution import histogram


@pytest.mark.parametrize(
    ("letters", "expected"),
    [
        pytest.param("a b c", {"a": 1, "b": 1, "c": 1}, id="example-all-tied"),
        pytest.param("a b b a", {"a": 2, "b": 2}, id="example-two-tied"),
        pytest.param("a b c a b", {"a": 2, "b": 2}, id="example-exclude-minority"),
        pytest.param("b b b b a", {"b": 4}, id="example-single-winner"),
        pytest.param("z", {"z": 1}, id="single-letter"),
        pytest.param("x x x x x", {"x": 5}, id="one-repeated-letter"),
        pytest.param("z a m", {"z": 1, "a": 1, "m": 1}, id="distinct-unsorted"),
        pytest.param("a a b c", {"a": 2}, id="winner-at-start"),
        pytest.param("a b b c", {"b": 2}, id="winner-in-middle"),
        pytest.param("a b c c", {"c": 2}, id="winner-at-end"),
        pytest.param(
            "a b c a b c d", {"a": 2, "b": 2, "c": 2}, id="three-winners"
        ),
        pytest.param(
            "a a a b b c c c d", {"a": 3, "c": 3}, id="different-minority-counts"
        ),
        pytest.param(
            "c b a c d a b c a", {"a": 3, "c": 3}, id="interleaved-winners"
        ),
        pytest.param(
            " ".join("abcdefghijklmnopqrstuvwxyz"),
            {letter: 1 for letter in "abcdefghijklmnopqrstuvwxyz"},
            id="whole-alphabet-tied",
        ),
    ],
)
def test_histogram_returns_only_letters_with_the_highest_count(letters, expected):
    assert histogram(letters) == expected


def test_histogram_empty_string_returns_empty_dictionary():
    assert histogram("") == {}


def test_histogram_calls_do_not_share_counts_or_results():
    first = histogram("a a b")
    second = histogram("b b b a")

    assert first == {"a": 2}
    assert second == {"b": 3}
    first["b"] = 99
    assert second == {"b": 3}
    assert histogram("a a b") == {"a": 2}
