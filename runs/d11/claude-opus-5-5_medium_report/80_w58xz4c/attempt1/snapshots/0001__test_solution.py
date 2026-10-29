import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    "lst, expected",
    [
        # Docstring examples
        (["aa", "a", "aaa"], ["aa"]),
        (["ab", "a", "aaa", "cd"], ["ab", "cd"]),
        # Empty and all-odd inputs
        ([], []),
        (["a", "abc", "abcde"], []),
        # Sort by length first, then alphabetically
        (["dddd", "cc", "bbbb", "aa"], ["aa", "cc", "bbbb", "dddd"]),
        (["abcd", "ab", "a"], ["ab", "abcd"]),
        (["zz", "aaaa", "yy"], ["yy", "zz", "aaaa"]),
        # Duplicates are kept
        (["bb", "aa", "bb", "aa"], ["aa", "aa", "bb", "bb"]),
        # Empty string has even length (0) and sorts first
        (["ab", "", "c"], ["", "ab"]),
        # Alphabetical tie-break is plain string ordering (uppercase before lowercase)
        (["ba", "Ab", "ab"], ["Ab", "ab", "ba"]),
        # Mixed lengths
        (["school", "AI", "asdf", "b"], ["AI", "asdf", "school"]),
        (["d", "dcba", "abcd", "a"], ["abcd", "dcba"]),
        (["AI", "ai", "au"], ["AI", "ai", "au"]),
        (["a", "b", "b", "c", "c", "a"], []),
        (["aaaa", "bbbb", "dd", "cc"], ["cc", "dd", "aaaa", "bbbb"]),
    ],
)
def test_sorted_list_sum(lst, expected):
    assert sorted_list_sum(lst) == expected


def test_returns_list_of_strings():
    result = sorted_list_sum(["xy", "z", "abcd"])
    assert isinstance(result, list)
    assert all(isinstance(s, str) for s in result)


def test_result_is_new_list_object():
    lst = ["aa", "bb"]
    result = sorted_list_sum(lst)
    assert result is not lst
