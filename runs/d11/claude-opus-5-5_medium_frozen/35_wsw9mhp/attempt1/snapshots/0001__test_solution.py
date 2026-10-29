import pytest

from solution import reverse_delete

BUG = (
    "solution.py inverts the palindrome check: it returns `s[::-1] != s` "
    "instead of `s[::-1] == s`"
)


# --- Deletion behaviour (first tuple element) -------------------------------

@pytest.mark.parametrize(
    "s, c, expected",
    [
        ("abcde", "ae", "bcd"),
        ("abcdef", "b", "acdef"),
        ("abcdedcba", "ab", "cdedc"),
        ("dwik", "w", "dik"),
        ("a", "a", ""),
        ("abcdedcba", "", "abcdedcba"),
        ("abcdedcba", "v", "abcdedcba"),
        ("vabba", "v", "abba"),
        ("mamma", "mia", ""),
        ("", "abc", ""),
        ("", "", ""),
        ("aaaa", "a", ""),
        ("AaBb", "a", "ABb"),  # case-sensitive
        ("a b a", " ", "aba"),
    ],
)
def test_deleted_string(s, c, expected):
    assert reverse_delete(s, c)[0] == expected


def test_returns_tuple_of_str_and_bool():
    result = reverse_delete("abcde", "ae")
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], bool)


def test_does_not_mutate_inputs():
    s, c = "abcde", "ae"
    reverse_delete(s, c)
    assert (s, c) == ("abcde", "ae")


def test_duplicate_chars_in_c_are_harmless():
    assert reverse_delete("abcde", "aaee")[0] == reverse_delete("abcde", "ae")[0]


# --- Palindrome flag (second tuple element), per the docstring spec ---------

PALINDROME_CASES = [
    ("abcde", "ae", ("bcd", False)),
    ("abcdef", "b", ("acdef", False)),
    ("abcdedcba", "ab", ("cdedc", True)),
    ("dwik", "w", ("dik", False)),
    ("a", "a", ("", True)),
    ("abcdedcba", "", ("abcdedcba", True)),
    ("abcdedcba", "v", ("abcdedcba", True)),
    ("vabba", "v", ("abba", True)),
    ("mamma", "mia", ("", True)),
]


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("s, c, expected", PALINDROME_CASES)
def test_full_result_matches_spec(s, c, expected):
    assert reverse_delete(s, c) == expected


def test_palindrome_flag_is_currently_inverted():
    """Pins the current (buggy) behaviour so a change is noticed.

    Delete this test once solution.py is fixed; the xfail tests above
    will then start failing (strict) and should have their marker removed.
    """
    for s, c, (_, is_pal) in PALINDROME_CASES:
        assert reverse_delete(s, c)[1] is (not is_pal)
