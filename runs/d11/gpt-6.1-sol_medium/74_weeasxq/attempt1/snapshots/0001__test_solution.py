import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        pytest.param([], [], id="empty-list"),
        pytest.param(["a", "aaa", "abcde"], [], id="all-odd-lengths"),
        pytest.param(["aa", "a", "aaa"], ["aa"], id="first-docstring-example"),
        pytest.param(
            ["ab", "a", "aaa", "cd"],
            ["ab", "cd"],
            id="second-docstring-example",
        ),
        pytest.param(["zz", "ab", "ba"], ["ab", "ba", "zz"], id="alphabetical-ties"),
        pytest.param(
            ["aaaa", "zz", "bbbbbb", "bb", "cccc", "a"],
            ["bb", "zz", "aaaa", "cccc", "bbbbbb"],
            id="length-before-alphabetical-order",
        ),
        pytest.param(["bb", "aa", "bb", "a", "a"], ["aa", "bb", "bb"], id="duplicates"),
        pytest.param(["bb", "", "a", ""], ["", "", "bb"], id="empty-strings"),
        pytest.param(["bb", "AA", "Aa", "aa"], ["AA", "Aa", "aa", "bb"], id="case-sensitive-order"),
        pytest.param(["éé", "é", "öö", "aa"], ["aa", "éé", "öö"], id="unicode-strings"),
        pytest.param(["  ", "a ", " "], ["  ", "a "], id="whitespace-counts-toward-length"),
        pytest.param(["abcd"], ["abcd"], id="single-even-string"),
    ],
)
def test_sorted_list_sum(words, expected):
    result = sorted_list_sum(words)

    assert isinstance(result, list)
    assert result == expected
