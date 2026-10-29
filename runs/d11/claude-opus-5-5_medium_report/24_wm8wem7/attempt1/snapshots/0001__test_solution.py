import pytest
from solution import is_sorted


@pytest.mark.parametrize("lst, expected", [
    ([5], True),
    ([1, 2, 3, 4, 5], True),
    ([1, 3, 2, 4, 5], False),
    ([1, 2, 3, 4, 5, 6], True),
    ([1, 2, 3, 4, 5, 6, 7], True),
    ([1, 3, 2, 4, 5, 6, 7], False),
    ([1, 2, 2, 3, 3, 4], True),
    ([1, 2, 2, 2, 3, 4], False),
])
def test_docstring_examples(lst, expected):
    assert is_sorted(lst) is expected


def test_empty_list_is_sorted():
    assert is_sorted([]) is True


def test_single_zero():
    assert is_sorted([0]) is True


def test_two_equal_elements_allowed():
    assert is_sorted([3, 3]) is True


def test_three_equal_elements_rejected():
    assert is_sorted([3, 3, 3]) is False


def test_triplicate_anywhere_rejected_even_if_ascending():
    assert is_sorted([0, 0, 0, 1]) is False
    assert is_sorted([1, 2, 9, 9, 9]) is False


def test_descending_is_not_sorted():
    assert is_sorted([5, 4, 3, 2, 1]) is False
    assert is_sorted([2, 1]) is False


def test_unsorted_at_end():
    assert is_sorted([1, 2, 3, 5, 4]) is False


def test_unsorted_with_duplicates():
    assert is_sorted([2, 2, 1]) is False


def test_triplicate_non_adjacent_rejected():
    # Three occurrences of the same number in an unsorted list -> False
    assert is_sorted([1, 2, 1, 1]) is False


def test_large_gaps_and_numbers():
    assert is_sorted([0, 10, 1000, 10**9]) is True


def test_does_not_mutate_input():
    data = [1, 3, 2]
    is_sorted(data)
    assert data == [1, 3, 2]
