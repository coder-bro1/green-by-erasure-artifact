import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["aa", "a", "aaa"], ["aa"]),
        (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
        (["pear", "fig", "plum", "kiwi", "apple"], ["kiwi", "pear", "plum"]),
        (["zz", "aa", "bb", "a", "cc", "bb"], ["aa", "bb", "bb", "cc", "zz"]),
        ([], []),
        (["odd", "words", "only", "even"], ["even", "only"]),
    ],
)
def test_sorted_list_sum(words, expected):
    assert sorted_list_sum(words) == expected
