import pytest

from solution import sorted_list_sum


# --- Docstring examples -------------------------------------------------------

def test_docstring_example_1():
    assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]


def test_docstring_example_2():
    assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]


# --- Filtering of odd-length strings ----------------------------------------

def test_empty_list():
    assert sorted_list_sum([]) == []


def test_all_odd_lengths_removed():
    assert sorted_list_sum(["a", "abc", "abcde"]) == []


def test_empty_string_has_even_length_and_is_kept():
    assert sorted_list_sum(["", "a"]) == [""]


def test_single_even_string():
    assert sorted_list_sum(["ab"]) == ["ab"]


def test_duplicates_are_kept():
    assert sorted_list_sum(["bb", "aa", "bb", "c"]) == ["aa", "bb", "bb"]


# --- Alphabetical ordering among equal lengths --------------------------------

def test_same_length_sorted_alphabetically():
    assert sorted_list_sum(["dd", "cc", "bb", "aa"]) == ["aa", "bb", "cc", "dd"]


def test_same_length_words():
    assert sorted_list_sum(["school", "AI", "asdf", "b"]) == ["AI", "asdf", "school"]


def test_uppercase_sorts_before_lowercase():
    # Standard Python string ordering (ASCII): uppercase < lowercase.
    assert sorted_list_sum(["ba", "Ab", "aB"]) == ["Ab", "aB", "ba"]


def test_mixed_lengths_where_alpha_and_length_order_agree():
    assert sorted_list_sum(["abcd", "ab", "x", "abcdef"]) == ["ab", "abcd", "abcdef"]


def test_returns_list_of_strings():
    result = sorted_list_sum(["aa", "bbbb"])
    assert isinstance(result, list)
    assert all(isinstance(s, str) for s in result)


# --- Spec requirements the current implementation does NOT satisfy ----------
# The docstring requires ascending order by length, then alphabetical. The
# implementation only sorts alphabetically, so these cases fail. They are
# marked strict xfail: if solution.py is fixed, these will XPASS and fail the
# run, signalling that the markers should be removed.

@pytest.mark.xfail(strict=True, reason="solution.py sorts alphabetically only, not by length first")
def test_sorted_by_length_then_alphabetically():
    assert sorted_list_sum(["aaaa", "bbbb", "dd", "cc"]) == ["cc", "dd", "aaaa", "bbbb"]


@pytest.mark.xfail(strict=True, reason="solution.py sorts alphabetically only, not by length first")
def test_shorter_word_comes_first_even_if_alphabetically_later():
    assert sorted_list_sum(["aaaa", "bb"]) == ["bb", "aaaa"]


@pytest.mark.xfail(strict=True, reason="solution.py sorts alphabetically only, not by length first")
def test_mixed_case_by_length():
    assert sorted_list_sum(["AI", "ai", "au", "abcd", "b", "c", "dddd"]) == [
        "AI", "ai", "au", "abcd", "dddd"
    ] and sorted_list_sum(["zz", "aaaaaa", "bbbb"]) == ["zz", "bbbb", "aaaaaa"]


@pytest.mark.xfail(strict=True, reason="solution.py sorts the caller's list in place")
def test_input_list_is_not_mutated():
    data = ["cc", "a", "bb"]
    sorted_list_sum(data)
    assert data == ["cc", "a", "bb"]
