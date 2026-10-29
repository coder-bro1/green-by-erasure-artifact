import random

import pytest

from solution import quicksort


DUPLICATES_BUG = (
    "Known bug in solution.py: elements equal to the pivot (other than the "
    "pivot itself) are discarded, so duplicate values are lost."
)


def test_empty_list():
    assert quicksort([]) == []


def test_single_element():
    assert quicksort([42]) == [42]


def test_already_sorted():
    assert quicksort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_reverse_sorted():
    assert quicksort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_unsorted_distinct():
    assert quicksort([3, 1, 4, 5, 9, 2, 6]) == [1, 2, 3, 4, 5, 6, 9]


def test_negative_numbers():
    assert quicksort([0, -3, 7, -1, 2]) == [-3, -1, 0, 2, 7]


def test_two_elements():
    assert quicksort([2, 1]) == [1, 2]
    assert quicksort([1, 2]) == [1, 2]


def test_does_not_mutate_input():
    data = [3, 1, 2]
    quicksort(data)
    assert data == [3, 1, 2]


def test_returns_new_list():
    data = [1]
    result = quicksort(data)
    assert result == data
    assert result is not data


@pytest.mark.parametrize("seed", range(20))
def test_random_distinct_matches_sorted(seed):
    rng = random.Random(seed)
    data = rng.sample(range(-1000, 1000), rng.randint(0, 100))
    assert quicksort(data) == sorted(data)


@pytest.mark.xfail(reason=DUPLICATES_BUG, strict=True)
def test_duplicates_preserved():
    assert quicksort([3, 1, 2, 3, 1]) == [1, 1, 2, 3, 3]


@pytest.mark.xfail(reason=DUPLICATES_BUG, strict=True)
def test_all_equal():
    assert quicksort([7, 7, 7]) == [7, 7, 7]


@pytest.mark.xfail(reason=DUPLICATES_BUG, strict=True)
def test_output_length_matches_input_with_duplicates():
    data = [5, 5, 1, 2, 2]
    assert len(quicksort(data)) == len(data)
