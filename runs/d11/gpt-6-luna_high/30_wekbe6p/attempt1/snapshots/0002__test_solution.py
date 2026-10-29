import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["aa", "a", "aaa"], ["aa"]),
        (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
        (["longer", "four", "to", "six", "one"], ["to", "four", "longer"]),
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
        "pear",
        "plum",
    ]


def test_sorted_list_sum_preserves_duplicates():
    assert sorted_list_sum(["bb", "aa", "bb", "a"]) == ["aa", "bb", "bb"]
