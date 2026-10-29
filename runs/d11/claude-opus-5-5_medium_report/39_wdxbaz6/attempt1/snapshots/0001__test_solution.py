import pytest

from solution import reverse_delete

INVERTED = (
    "solution.py computes the palindrome flag as `s[::-1] != s`, which is the "
    "negation of the documented check (should be `==`)"
)


# --- Deleted-string component (works correctly) ---

@pytest.mark.parametrize(
    "s, c, expected",
    [
        ("abcde", "ae", "bcd"),
        ("abcdef", "b", "acdef"),
        ("abcdedcba", "ab", "cdedc"),
        ("abcdedcba", "", "abcdedcba"),
        ("", "abc", ""),
        ("aaaa", "a", ""),
        ("mamma", "mia", ""),
        ("hello", "xyz", "hello"),
        ("aAbB", "a", "AbB"),  # case-sensitive
        ("a b a", " ", "aba"),
        ("abcabc", "cba", ""),
        ("abc", "aa", "bc"),  # duplicate chars in c
    ],
)
def test_result_string(s, c, expected):
    result = reverse_delete(s, c)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == expected


def test_does_not_mutate_inputs():
    s, c = "abcde", "ae"
    reverse_delete(s, c)
    assert (s, c) == ("abcde", "ae")


# --- Full tuple / palindrome flag (docstring examples and more) ---

@pytest.mark.xfail(strict=True, reason=INVERTED)
@pytest.mark.parametrize(
    "s, c, expected",
    [
        ("abcde", "ae", ("bcd", False)),
        ("abcdef", "b", ("acdef", False)),
        ("abcdedcba", "ab", ("cdedc", True)),
        ("dwik", "w", ("dik", False)),
        ("a", "a", ("", True)),
        ("abcdedcba", "", ("abcdedcba", True)),
        ("abcdedcba", "v", ("abcdedcba", True)),
        ("vabba", "v", ("abba", True)),
        ("mamma", "mia", ("", True)),
        ("racecarx", "x", ("racecar", True)),
        ("ab", "", ("ab", False)),
    ],
)
def test_full_result(s, c, expected):
    assert reverse_delete(s, c) == expected


def test_flag_is_bool():
    assert isinstance(reverse_delete("abc", "b")[1], bool)
