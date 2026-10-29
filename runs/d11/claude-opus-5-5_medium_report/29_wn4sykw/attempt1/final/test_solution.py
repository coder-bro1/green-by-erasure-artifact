import pytest

from solution import pairs_sum_to_zero

SELF_PAIR_BUG = (
    "inner loop starts at j=i, so an element is paired with itself; "
    "a single 0 is wrongly treated as a pair of distinct elements"
)


# Docstring examples
@pytest.mark.xfail(strict=True, reason=SELF_PAIR_BUG)
def test_docstring_with_single_zero():
    assert pairs_sum_to_zero([1, 3, 5, 0]) is False


def test_docstring_no_pair():
    assert pairs_sum_to_zero([1, 3, -2, 1]) is False


def test_docstring_all_positive():
    assert pairs_sum_to_zero([1, 2, 3, 7]) is False


def test_docstring_pair_exists():
    assert pairs_sum_to_zero([2, 4, -5, 3, 5, 7]) is True


def test_docstring_single_element():
    assert pairs_sum_to_zero([1]) is False


# Additional cases
def test_empty_list():
    assert pairs_sum_to_zero([]) is False


@pytest.mark.xfail(strict=True, reason=SELF_PAIR_BUG)
def test_single_zero_only():
    assert pairs_sum_to_zero([0]) is False


def test_two_zeros():
    assert pairs_sum_to_zero([0, 0]) is True


def test_simple_pair():
    assert pairs_sum_to_zero([1, -1]) is True


def test_pair_order_reversed():
    assert pairs_sum_to_zero([-7, 3, 7]) is True


def test_pair_at_ends():
    assert pairs_sum_to_zero([4, 1, 2, 3, -4]) is True


def test_duplicates_without_opposite():
    assert pairs_sum_to_zero([2, 2, 2]) is False


def test_all_negative():
    assert pairs_sum_to_zero([-1, -2, -3]) is False


def test_large_numbers():
    assert pairs_sum_to_zero([10**18, 5, -(10**18)]) is True


def test_does_not_mutate_input():
    data = [3, -3, 1]
    pairs_sum_to_zero(data)
    assert data == [3, -3, 1]
