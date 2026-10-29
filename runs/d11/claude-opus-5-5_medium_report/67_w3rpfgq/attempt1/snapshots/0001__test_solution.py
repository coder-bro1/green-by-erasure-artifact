import pytest

from solution import will_it_fly

PALINDROME_BUG = (
    "solution.py inverts the palindrome check: it returns False when "
    "q[i] == q[j] instead of when q[i] != q[j]"
)


# --- Docstring examples ---

@pytest.mark.xfail(strict=True, reason=PALINDROME_BUG)
def test_docstring_unbalanced():
    assert will_it_fly([1, 2], 5) is False


def test_docstring_balanced_too_heavy():
    assert will_it_fly([3, 2, 3], 1) is False


@pytest.mark.xfail(strict=True, reason=PALINDROME_BUG)
def test_docstring_balanced_light_enough():
    assert will_it_fly([3, 2, 3], 9) is True


def test_docstring_single_element():
    assert will_it_fly([3], 5) is True


# --- Weight boundary ---

def test_single_element_exactly_at_limit():
    assert will_it_fly([5], 5) is True


def test_single_element_over_limit():
    assert will_it_fly([6], 5) is False


@pytest.mark.xfail(strict=True, reason=PALINDROME_BUG)
def test_palindrome_sum_equal_to_limit():
    assert will_it_fly([3, 2, 3], 8) is True


def test_palindrome_sum_one_over_limit():
    assert will_it_fly([3, 2, 3], 7) is False


def test_non_palindrome_over_limit():
    assert will_it_fly([1, 2, 3], 1) is False


# --- Balance ---

def test_empty_list_flies():
    assert will_it_fly([], 0) is True


@pytest.mark.xfail(strict=True, reason=PALINDROME_BUG)
def test_two_equal_elements():
    assert will_it_fly([2, 2], 10) is True


@pytest.mark.xfail(strict=True, reason=PALINDROME_BUG)
def test_even_length_palindrome():
    assert will_it_fly([1, 2, 2, 1], 10) is True


@pytest.mark.xfail(strict=True, reason=PALINDROME_BUG)
def test_non_palindrome_with_matching_ends_inner_mismatch():
    # Inner pair (2, 3) mismatches; outer pair matches.
    assert will_it_fly([1, 2, 3, 1], 10) is False


@pytest.mark.xfail(strict=True, reason=PALINDROME_BUG)
def test_non_palindrome_odd_length():
    assert will_it_fly([1, 2, 3], 10) is False


def test_non_palindrome_outer_mismatch_inner_match():
    # Outer mismatch, inner match: the bug happens to give the right answer.
    assert will_it_fly([1, 2, 2, 3], 10) is False
