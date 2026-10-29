import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    "lst, expected",
    [
        ([1, 3, 5, 0], False),
        ([1, 3, -2, 1], False),
        ([1, 2, 3, 7], False),
        ([2, 4, -5, 3, 5, 7], True),
        ([1], False),
    ],
)
def test_docstring_examples(lst, expected):
    assert pairs_sum_to_zero(lst) is expected


def test_empty_list():
    assert pairs_sum_to_zero([]) is False


def test_single_zero_is_not_a_pair():
    assert pairs_sum_to_zero([0]) is False


def test_two_zeros_are_distinct_elements():
    assert pairs_sum_to_zero([0, 0]) is True


def test_simple_pair():
    assert pairs_sum_to_zero([5, -5]) is True


def test_pair_at_ends():
    assert pairs_sum_to_zero([7, 1, 2, 3, -7]) is True


def test_same_element_not_used_twice():
    # 3 + 3 != 0 and no -3 present
    assert pairs_sum_to_zero([3, 1, 2]) is False


def test_duplicates_without_opposite():
    assert pairs_sum_to_zero([2, 2, 2]) is False


def test_all_negative():
    assert pairs_sum_to_zero([-1, -2, -3]) is False


def test_large_numbers():
    assert pairs_sum_to_zero([10**18, 3, -(10**18)]) is True


def test_does_not_mutate_input():
    data = [4, -1, 2, -4]
    copy = list(data)
    pairs_sum_to_zero(data)
    assert data == copy


def test_accepts_tuple():
    assert pairs_sum_to_zero((1, -1)) is True
