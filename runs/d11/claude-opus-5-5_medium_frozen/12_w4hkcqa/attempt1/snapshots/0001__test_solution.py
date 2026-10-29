import pytest

from solution import will_it_fly

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py bug: palindrome check uses '==' instead of '!=' "
    "(returns False on matching ends)",
)


# --- Behaviour that is correct in the current implementation ---

def test_docstring_balanced_but_too_heavy():
    assert will_it_fly([3, 2, 3], 1) is False


def test_docstring_single_element():
    assert will_it_fly([3], 5) is True


def test_empty_list_flies():
    assert will_it_fly([], 0) is True


def test_single_element_exact_weight():
    assert will_it_fly([5], 5) is True


def test_single_element_over_weight():
    assert will_it_fly([6], 5) is False


@pytest.mark.parametrize("q,w", [([1, 2], 2), ([5, 5], 9), ([1, 2, 1], 3)])
def test_over_weight_always_false(q, w):
    assert will_it_fly(q, w) is False


def test_negative_weight_limit():
    assert will_it_fly([], -1) is False


# --- Spec behaviour that fails because of the palindrome bug ---

@BUG
def test_docstring_unbalanced():
    assert will_it_fly([1, 2], 5) is False


@BUG
def test_docstring_balanced_and_light_enough():
    assert will_it_fly([3, 2, 3], 9) is True


@BUG
@pytest.mark.parametrize("q,w", [([2, 2], 4), ([1, 2, 1], 4), ([1, 2, 2, 1], 6)])
def test_palindrome_within_weight_flies(q, w):
    assert will_it_fly(q, w) is True


@BUG
@pytest.mark.parametrize("q,w", [([1, 2, 3], 6), ([1, 2, 3, 2], 100)])
def test_non_palindrome_within_weight_does_not_fly(q, w):
    assert will_it_fly(q, w) is False
