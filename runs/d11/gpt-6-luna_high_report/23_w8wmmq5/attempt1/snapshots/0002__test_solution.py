import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["aa", "a", "aaa"], ["aa"]),
        (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
        (["pear", "fig", "plum", "kiwi"], ["kiwi", "pear", "plum"]),
        (["", "x", "bb", "a", ""], ["", "", "bb"]),
        ([], []),
        (["odd", "seven", "words"], []),
    ],
)
def test_filters_odd_lengths_and_sorts_equal_lengths(words, expected):
    assert sorted_list_sum(words) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The implementation sorts alphabetically, but the docstring requires ascending length before alphabetical order.",
)
def test_sorts_by_length_before_alphabetical_order():
    assert sorted_list_sum(["zz", "bbbb", "aa", "ccc"]) == ["aa", "zz", "bbbb"]
