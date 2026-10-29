import pytest

from solution import even_length_words_sorted


# --- Behaviour that the current implementation gets right ---

def test_docstring_example():
    assert even_length_words_sorted(['dd', 'c', 'ab', 'eeee']) == ['ab', 'dd', 'eeee']


def test_empty_list():
    assert even_length_words_sorted([]) == []


def test_all_odd_lengths_removed():
    assert even_length_words_sorted(['a', 'abc', 'abcde']) == []


def test_empty_string_is_even_length():
    assert even_length_words_sorted(['', 'a']) == ['']


def test_equal_length_sorted_alphabetically():
    assert even_length_words_sorted(['dc', 'ba', 'ab', 'cd']) == ['ab', 'ba', 'cd', 'dc']


def test_duplicates_kept():
    assert even_length_words_sorted(['ab', 'ab', 'c']) == ['ab', 'ab']


def test_returns_list():
    assert isinstance(even_length_words_sorted(['ab']), list)


# --- Spec requirements the current implementation violates ---
# strict=True: if solution.py is fixed, these will XPASS and fail the run,
# signalling that the xfail markers should be removed.

@pytest.mark.xfail(strict=True, reason="BUG: sorts alphabetically only, not by length first")
def test_sorted_by_length_first():
    assert even_length_words_sorted(['zz', 'aaaa']) == ['zz', 'aaaa']


@pytest.mark.xfail(strict=True, reason="BUG: sorts alphabetically only, not by length first")
def test_length_then_alphabetical_mixed():
    words = ['bbbb', 'aa', 'cc', 'aaaa', 'b', 'zz', 'abcdef']
    assert even_length_words_sorted(words) == ['aa', 'cc', 'zz', 'aaaa', 'bbbb', 'abcdef']


@pytest.mark.xfail(strict=True, reason="BUG: mutates the caller's list via words.sort()")
def test_input_not_mutated():
    words = ['dd', 'c', 'ab']
    even_length_words_sorted(words)
    assert words == ['dd', 'c', 'ab']
