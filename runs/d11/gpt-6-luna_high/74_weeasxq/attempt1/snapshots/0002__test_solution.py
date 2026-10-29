import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        (["a", "bb", "ccc"], ["bb"]),
        (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
        (["long", "a", "bb", "ccc", "dddd"], ["bb", "dddd", "long"]),
        (["zz", "aa", "bb", "aa"], ["aa", "aa", "bb", "zz"]),
        ([], []),
    ],
)
def test_sorted_list_sum(words, expected):
    assert sorted_list_sum(words) == expected


def test_sorted_list_sum_does_not_modify_input():
    words = ["zz", "a", "bb"]

    sorted_list_sum(words)

    assert words == ["zz", "a", "bb"]
