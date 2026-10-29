import pytest

from solution import ascending_with_few_repeats


# --- Docstring examples ---

def test_docstring_sorted_with_one_pair():
    assert ascending_with_few_repeats([0, 4, 4, 9]) is True


def test_docstring_triple_repeat():
    assert ascending_with_few_repeats([3, 3, 3]) is False


def test_docstring_descending_pair():
    assert ascending_with_few_repeats([2, 1]) is False


def test_docstring_single_element():
    assert ascending_with_few_repeats([7]) is True


# --- Ordering ---

def test_empty_list():
    assert ascending_with_few_repeats([]) is True


@pytest.mark.parametrize("nums", [
    [0, 1, 2, 3],
    [0, 0],
    [1, 1, 2, 2, 3, 3],
    [5, 10, 100, 1000],
    [0, 0, 1],
])
def test_non_decreasing_with_at_most_two_repeats(nums):
    assert ascending_with_few_repeats(nums) is True


@pytest.mark.parametrize("nums", [
    [1, 0],
    [0, 2, 1],
    [1, 2, 3, 2],
    [5, 4, 3, 2, 1],
    [1, 1, 0],
])
def test_out_of_order(nums):
    assert ascending_with_few_repeats(nums) is False


# --- Repeat limit (no value more than twice) ---

@pytest.mark.parametrize("nums", [
    [0, 0, 0],
    [1, 2, 2, 2, 3],
    [4, 4, 4, 4],
    [1, 1, 2, 2, 3, 3, 3],
    [0, 0, 0, 5],
])
def test_value_appears_more_than_twice(nums):
    assert ascending_with_few_repeats(nums) is False


def test_exactly_two_repeats_allowed_for_every_value():
    assert ascending_with_few_repeats([0, 0, 1, 1, 2, 2]) is True


# --- Misc ---

def test_returns_bool():
    assert isinstance(ascending_with_few_repeats([1, 2]), bool)


def test_does_not_mutate_input():
    nums = [0, 4, 4, 9]
    ascending_with_few_repeats(nums)
    assert nums == [0, 4, 4, 9]


def test_large_sorted_input():
    nums = [i // 2 for i in range(10_000)]  # each value exactly twice
    assert ascending_with_few_repeats(nums) is True
