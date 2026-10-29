import pytest

from solution import sorted_list_sum


@pytest.mark.parametrize(
    ("words", "expected"),
    [
        pytest.param([], [], id="empty-input"),
        pytest.param(["aa", "a", "aaa"], ["aa"], id="first-docstring-example"),
        pytest.param(
            ["ab", "a", "aaa", "cd"],
            ["ab", "cd"],
            id="second-docstring-example",
        ),
        pytest.param(["z", "a", "b"], [], id="all-odd-single-characters"),
        pytest.param(["cat", "dog", "ant"], [], id="all-odd-words"),
        pytest.param(["ab"], ["ab"], id="single-even-word"),
        pytest.param(["zz", "ab", "aa"], ["aa", "ab", "zz"], id="alphabetical-order"),
        pytest.param(
            ["pear", "kiwi", "plum", "lime"],
            ["kiwi", "lime", "pear", "plum"],
            id="longer-even-words",
        ),
        pytest.param(
            ["bb", "aa", "bb", "aa"],
            ["aa", "aa", "bb", "bb"],
            id="preserve-even-duplicates",
        ),
        pytest.param(["a", "aa", "a", "aa"], ["aa", "aa"], id="remove-odd-duplicates"),
        pytest.param(["", "a", ""], ["", ""], id="empty-strings-have-even-length"),
        pytest.param(["ab", "Aa", "AA", "aA"], ["AA", "Aa", "aA", "ab"], id="case-sensitive-order"),
        pytest.param(["bb", "!!", "  "], ["  ", "!!", "bb"], id="punctuation-and-spaces"),
        pytest.param(["éé", "aa", "öö", "猫猫"], ["aa", "éé", "öö", "猫猫"], id="unicode-strings"),
        pytest.param(["猫", "é", "😀"], [], id="unicode-odd-length"),
        pytest.param(["aa", "bb", "cc"], ["aa", "bb", "cc"], id="already-sorted"),
    ],
)
def test_sorted_list_sum(words, expected):
    result = sorted_list_sum(words)

    assert isinstance(result, list)
    assert result == expected
