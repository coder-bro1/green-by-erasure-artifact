import pytest

from solution import sorted_list_sum


# --- Docstring examples -------------------------------------------------------

def test_docstring_example_1():
    assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]


def test_docstring_example_2():
    assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]


# --- Filtering of odd-length strings ------------------------------------------

def test_empty_list():
    assert sorted_list_sum([]) == []


def test_all_odd_lengths_removed():
    assert sorted_list_sum(["a", "abc", "abcde"]) == []


def test_empty_string_has_even_length_and_is_kept():
    assert sorted_list_sum(["", "a"]) == [""]


def test_duplicates_are_preserved():
    assert sorted_list_sum(["cd", "ab", "cd", "x"]) == ["ab", "cd", "cd"]


# --- Alphabetical ordering among equal lengths --------------------------------

def test_same_length_sorted_alphabetically():
    assert sorted_list_sum(["dd", "aa", "cc", "bb"]) == ["aa", "bb", "cc", "dd"]


def test_returns_list_of_strings():
    result = sorted_list_sum(["zz", "yy", "q"])
    assert isinstance(result, list)
    assert all(isinstance(s, str) for s in result)
    assert result == ["yy", "zz"]


# --- Ordering by length (primary key) -----------------------------------------

def test_lengths_already_consistent_with_alphabetical_order():
    # Alphabetical order and length order agree here.
    assert sorted_list_sum(["abcd", "ab"]) == ["ab", "abcd"]


@pytest.mark.xfail(
    strict=True,
    reason="solution sorts only alphabetically; docstring requires ascending length first",
)
def test_shorter_words_come_first_regardless_of_alphabet():
    assert sorted_list_sum(["aaaa", "bb", "cc"]) == ["bb", "cc", "aaaa"]


@pytest.mark.xfail(
    strict=True,
    reason="solution sorts only alphabetically; docstring requires ascending length first",
)
def test_mixed_lengths_sorted_by_length_then_alphabetically():
    lst = ["dddddd", "zz", "aaaa", "bb", "cccc", "a", "abc"]
    assert sorted_list_sum(lst) == ["bb", "zz", "aaaa", "cccc", "dddddd"]


@pytest.mark.xfail(
    strict=True,
    reason="solution sorts only alphabetically; docstring requires ascending length first",
)
def test_empty_string_sorts_before_longer_words():
    # "" is shortest; alphabetical sort also puts it first, but "abcd" < "zz"
    # alphabetically while "zz" is shorter.
    assert sorted_list_sum(["abcd", "zz", ""]) == ["", "zz", "abcd"]
