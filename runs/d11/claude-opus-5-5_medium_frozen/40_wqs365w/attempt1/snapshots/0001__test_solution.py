import pytest

from solution import sum_product


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([], (0, 1)),
        ([1, 2, 3, 4], (10, 24)),
        ([5], (5, 5)),
        ([0], (0, 0)),
        ([1, 1, 1], (3, 1)),
        ([100, 0], (100, 0)),
        ([3, 5, 7], (15, 105)),
        ([10], (10, 10)),
        ([-1, -2, -3], (-6, -6)),
        ([-2, 4], (2, -8)),
    ],
)
def test_sum_product(numbers, expected):
    assert sum_product(numbers) == expected


def test_returns_tuple():
    assert isinstance(sum_product([1, 2]), tuple)


def test_sum_component():
    assert sum_product([1, 2, 3, 4])[0] == 10
    assert sum_product([])[0] == 0
    assert sum_product([-5, 5])[0] == 0


def test_large_values():
    nums = [10**6, 10**6, 10**6]
    assert sum_product(nums) == (3 * 10**6, 10**18)


def test_input_not_mutated():
    nums = [1, 2, 3]
    sum_product(nums)
    assert nums == [1, 2, 3]
