import pytest

from solution import rolling_max

BUG_REASON = (
    "rolling_max uses max(numbers) (max of the whole list) instead of "
    "max(running_max, n), so later elements leak into earlier positions"
)


def test_empty_list():
    assert rolling_max([]) == []


def test_single_element():
    assert rolling_max([7]) == [7]


def test_all_equal():
    assert rolling_max([3, 3, 3, 3]) == [3, 3, 3, 3]


def test_strictly_decreasing():
    assert rolling_max([4, 3, 2, 1]) == [4, 4, 4, 4]


def test_first_element_is_max():
    assert rolling_max([5, 1, 4, 2, 5]) == [5, 5, 5, 5, 5]


def test_negative_numbers_first_is_max():
    assert rolling_max([-1, -5, -3]) == [-1, -1, -1]


def test_does_not_mutate_input():
    data = [3, 2, 1]
    rolling_max(data)
    assert data == [3, 2, 1]


def test_output_length_matches_input():
    data = [9, 1, 8, 2, 7]
    assert len(rolling_max(data)) == len(data)


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
def test_docstring_example():
    assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
def test_strictly_increasing():
    assert rolling_max([1, 2, 3, 4]) == [1, 2, 3, 4]


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
def test_increasing_negatives():
    assert rolling_max([-5, -3, -4, -1]) == [-5, -3, -3, -1]


@pytest.mark.xfail(strict=True, reason=BUG_REASON)
def test_max_appears_late():
    assert rolling_max([2, 1, 10]) == [2, 2, 10]
