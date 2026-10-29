import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["aa", "a", "aaa"], ["aa"]),
        (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
    ],
)
def test_examples_filter_odd_length_words_and_sort(words, expected):
    assert sorted_list_sum(words) == expected


def test_keeps_even_length_words_in_alphabetical_order():
    # The documented input constraint says words have the same length.
    assert sorted_list_sum(["pear", "kiwi", "plum", "figs"]) == [
        "figs",
        "kiwi",
        "pear",
        "plum",
    ]


def test_preserves_duplicate_even_length_words():
    assert sorted_list_sum(["bb", "aa", "bb", "a"]) == ["aa", "bb", "bb"]


@pytest.mark.parametrize("words", [[], ["a", "xyz", "hello"]])
def test_returns_empty_list_when_there_are_no_even_length_words(words):
    assert sorted_list_sum(words) == []
