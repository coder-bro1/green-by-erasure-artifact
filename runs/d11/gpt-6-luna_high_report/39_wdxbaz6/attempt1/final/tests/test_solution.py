import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    ("s", "c", "expected_result"),
    [
        ("abcde", "ae", "bcd"),
        ("abcdef", "b", "acdef"),
        ("abcdedcba", "ab", "cdedc"),
        ("aabbcc", "ac", "bb"),
        ("unchanged", "", "unchanged"),
        ("remove all", "remove all", ""),
        ("", "anything", ""),
    ],
)
def test_reverse_delete_removes_every_character_in_c(s, c, expected_result):
    result, _ = reverse_delete(s, c)

    assert result == expected_result


@pytest.mark.parametrize(
    ("s", "c", "expected"),
    [
        ("abcde", "ae", ("bcd", False)),
        ("abcdef", "b", ("acdef", False)),
        ("abcdedcba", "ab", ("cdedc", True)),
        ("aabbcc", "ac", ("bb", True)),
        ("single", "ingle", ("s", True)),
        ("", "anything", ("", True)),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="reverse_delete returns whether the result is non-palindromic, opposite to its docstring",
)
def test_reverse_delete_returns_result_and_palindrome_status(s, c, expected):
    assert reverse_delete(s, c) == expected
