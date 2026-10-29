import pytest

from solution import even_length_words_sorted


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        ([], []),
        (["a", "cat", "seven"], []),
        (["dd", "c", "ab", "eeee"], ["ab", "dd", "eeee"]),
        (["zz", "bb", "aa"], ["aa", "bb", "zz"]),
        (["aa", "aa", "b", "aa"], ["aa", "aa", "aa"]),
        (["", "a", "bb", ""], ["", "", "bb"]),
        (["zz", "AA", "aa", "Bb"], ["AA", "Bb", "aa", "zz"]),
        (["  ", "a ", "!", "!?"], ["  ", "!?", "a "]),
        (["éé", "猫", "猫犬", "é"], ["éé", "猫犬"]),
        (["ab"], ["ab"]),
        (["abc"], []),
    ],
)
def test_filters_odd_lengths_and_sorts_alphabetically(words, expected):
    assert even_length_words_sorted(words) == expected


def test_current_order_is_alphabetical_even_when_lengths_differ():
    """Characterize the implementation's departure from its docstring."""
    assert even_length_words_sorted(["zz", "aaaa"]) == ["aaaa", "zz"]


def test_sorts_input_in_place_without_removing_odd_length_words():
    words = ["zz", "c", "aaaa", "b"]

    result = even_length_words_sorted(words)

    assert words == ["aaaa", "b", "c", "zz"]
    assert result == ["aaaa", "zz"]


def test_returns_a_separate_list():
    words = ["bb", "aa"]

    result = even_length_words_sorted(words)
    result.append("cc")

    assert result is not words
    assert words == ["aa", "bb"]


def test_empty_result_is_a_separate_list():
    words = []

    result = even_length_words_sorted(words)

    assert result == []
    assert result is not words
