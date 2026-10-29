import pytest

from solution import sum_product


def test_empty_list():
    assert sum_product([]) == (0, 1)


def test_docstring_example():
    assert sum_product([1, 2, 3, 4]) == (10, 24)


def test_single_element():
    assert sum_product([7]) == (7, 7)


def test_single_zero():
    assert sum_product([0]) == (0, 0)


def test_contains_zero():
    assert sum_product([3, 0, 5]) == (8, 0)


def test_all_ones():
    assert sum_product([1, 1, 1]) == (3, 1)


def test_negative_numbers():
    assert sum_product([-1, -2, -3]) == (-6, -6)


def test_mixed_signs():
    assert sum_product([-2, 3, 4]) == (5, -24)


def test_even_count_negatives_positive_product():
    assert sum_product([-2, -5]) == (-7, 10)


def test_large_numbers_no_overflow():
    assert sum_product([10**10, 10**10]) == (2 * 10**10, 10**20)


def test_returns_tuple_of_ints():
    result = sum_product([2, 3])
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, int) for x in result)


def test_does_not_mutate_input():
    data = [1, 2, 3]
    sum_product(data)
    assert data == [1, 2, 3]


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([100, 2, 3, 4], (109, 2400)),
        ([3, 5, 7], (15, 105)),
        ([10], (10, 10)),
        ([2] * 10, (20, 1024)),
    ],
)
def test_parametrized(numbers, expected):
    assert sum_product(numbers) == expected
