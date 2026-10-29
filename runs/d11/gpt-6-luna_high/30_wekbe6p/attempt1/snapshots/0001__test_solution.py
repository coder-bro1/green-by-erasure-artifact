import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["aa", "a", "aaa"], ["aa"]),
        (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
        (["four", "to", "six", "one"], ["to", "six", "one", "four"]),
        (["bbb", "a", "xyz"], []),
        ([], []),
    ],
)
def test_sorted_list_sum_filters_and_sorts(words, expected):
    assert sorted_list_sum(words) == expected


def test_sorted_list_sum_sorts_alphabetically_within_equal_lengths():
    assert sorted_list_sum(["pear", "kiwi", "plum", "figs"]) == [
        "figs",
        "kiwi",
        "plum",
        "pear",
    ]


def test_sorted_list_sum_preserves_duplicates():
    assert sorted_list_sum(["bb", "aa", "bb", "a"]) == ["aa", "bb", "bb"]
