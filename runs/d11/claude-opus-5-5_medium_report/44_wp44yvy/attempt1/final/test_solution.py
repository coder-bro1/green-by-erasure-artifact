import pytest

from solution import reverse_delete


@pytest.mark.parametrize(
    "s, c, expected",
    [
        # Docstring examples
        ("abcde", "ae", ("bcd", False)),
        ("abcdef", "b", ("acdef", False)),
        ("abcdedcba", "ab", ("cdedc", True)),
        # Additional cases
        ("dwik", "w", ("dik", False)),
        ("a", "a", ("", True)),
        ("abcdedcba", "", ("abcdedcba", True)),
        ("abcdedcba", "v", ("abcdedcba", True)),
        ("vabba", "v", ("abba", True)),
        ("mamma", "mia", ("", True)),
    ],
)
def test_reverse_delete(s, c, expected):
    assert reverse_delete(s, c) == expected


def test_empty_string():
    assert reverse_delete("", "abc") == ("", True)


def test_empty_both():
    assert reverse_delete("", "") == ("", True)


def test_deletes_all_occurrences():
    assert reverse_delete("aaabaaa", "a") == ("b", True)


def test_duplicate_chars_in_c():
    assert reverse_delete("abcba", "bbb") == ("aca", True)


def test_case_sensitive():
    assert reverse_delete("Abca", "a") == ("Abc", False)
    assert reverse_delete("Aba", "A") == ("ba", False)


def test_single_char_result_is_palindrome():
    assert reverse_delete("xyz", "xz") == ("y", True)


def test_even_length_palindrome():
    assert reverse_delete("abxba", "x") == ("abba", True)


def test_not_palindrome():
    assert reverse_delete("ab", "") == ("ab", False)


def test_returns_tuple_of_str_and_bool():
    result = reverse_delete("abc", "b")
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], bool)


def test_input_not_mutated():
    s, c = "abcde", "ae"
    reverse_delete(s, c)
    assert s == "abcde" and c == "ae"
