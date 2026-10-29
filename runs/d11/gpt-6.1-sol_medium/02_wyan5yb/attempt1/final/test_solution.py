import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    ("source", "characters", "expected"),
    [
        pytest.param("abcde", "ae", ("bcd", False), id="example-non-palindrome"),
        pytest.param("abcdef", "b", ("acdef", False), id="example-delete-one"),
        pytest.param("abcdedcba", "ab", ("cdedc", True), id="example-palindrome"),
        pytest.param("", "abc", ("", True), id="empty-source"),
        pytest.param("racecar", "", ("racecar", True), id="no-deletions-palindrome"),
        pytest.param("abc", "", ("abc", False), id="no-deletions-non-palindrome"),
        pytest.param("ababa", "ab", ("", True), id="delete-every-character"),
        pytest.param("abaca", "a", ("bc", False), id="delete-all-occurrences"),
        pytest.param("abaca", "aaa", ("bc", False), id="duplicate-deletion-characters"),
        pytest.param("abc", "ac", ("b", True), id="single-character-result"),
        pytest.param("abba", "xyz", ("abba", True), id="absent-deletion-characters"),
        pytest.param("AaA", "a", ("AA", True), id="case-sensitive-deletion"),
        pytest.param("Aa", "", ("Aa", False), id="case-sensitive-palindrome"),
        pytest.param("a b!a", " !", ("aba", True), id="spaces-and-punctuation"),
        pytest.param("\u00e9\u732b\u00e9", "\u732b", ("\u00e9\u00e9", True), id="unicode-characters"),
        pytest.param("cabdab", "ab", ("cd", False), id="delete-characters-not-substring"),
    ],
)
def test_reverse_delete(source, characters, expected):
    result = reverse_delete(source, characters)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == expected[0]
    assert result[1] is expected[1]
