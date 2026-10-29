import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        pytest.param([], [], id="empty-input"),
        pytest.param(["a", "abc", "abcde"], [], id="all-odd-lengths"),
        pytest.param(["aa", "a", "aaa"], ["aa"], id="first-example"),
        pytest.param(
            ["ab", "a", "aaa", "cd"], ["ab", "cd"], id="second-example"
        ),
        pytest.param(["even"], ["even"], id="single-even-word"),
        pytest.param(
            ["zz", "aa", "mm", "ab"],
            ["aa", "ab", "mm", "zz"],
            id="alphabetical-tiebreak",
        ),
        pytest.param(
            ["aaaaaa", "zz", "bbbb", "aa", "cccc", "x"],
            ["aa", "zz", "bbbb", "cccc", "aaaaaa"],
            id="length-before-alphabetical-order",
        ),
        pytest.param(
            ["bb", "a", "aa", "bb", "a", "aa"],
            ["aa", "aa", "bb", "bb"],
            id="preserve-even-duplicates",
        ),
        pytest.param(
            ["bb", "", "a", "aa", ""],
            ["", "", "aa", "bb"],
            id="empty-strings-have-even-length",
        ),
        pytest.param(
            ["aa", "BB", "Aa", "bb"],
            ["Aa", "BB", "aa", "bb"],
            id="case-sensitive-order",
        ),
        pytest.param(
            ["éé", "猫", "猫狗", "é", "aa"],
            ["aa", "éé", "猫狗"],
            id="unicode-character-lengths",
        ),
        pytest.param(
            ["12", "!!", "a b", "  ", "abcd"],
            ["  ", "!!", "12", "abcd"],
            id="whitespace-punctuation-and-digits",
        ),
    ],
)
def test_sorted_list_sum(words, expected):
    result = sorted_list_sum(words)

    assert isinstance(result, list)
    assert result == expected
