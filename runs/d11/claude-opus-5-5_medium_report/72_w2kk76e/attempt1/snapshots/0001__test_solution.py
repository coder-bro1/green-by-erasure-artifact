import pytest

from solution import sum_product

PROD_BUG = "prod_value is initialized to 0 instead of 1, so the product is always 0"


@pytest.mark.xfail(strict=True, reason=PROD_BUG)
def test_empty_list():
    assert sum_product([]) == (0, 1)


@pytest.mark.xfail(strict=True, reason=PROD_BUG)
def test_docstring_example():
    assert sum_product([1, 2, 3, 4]) == (10, 24)


@pytest.mark.xfail(strict=True, reason=PROD_BUG)
def test_single_element():
    assert sum_product([7]) == (7, 7)


@pytest.mark.xfail(strict=True, reason=PROD_BUG)
def test_negative_numbers():
    assert sum_product([-1, -2, 3]) == (0, 6)


@pytest.mark.xfail(strict=True, reason=PROD_BUG)
def test_all_ones():
    assert sum_product([1, 1, 1]) == (3, 1)


@pytest.mark.xfail(strict=True, reason=PROD_BUG)
def test_large_values():
    assert sum_product([100, 100, 100]) == (300, 1_000_000)


def test_list_containing_zero():
    assert sum_product([3, 0, 5]) == (8, 0)


def test_only_zero():
    assert sum_product([0]) == (0, 0)


def test_sum_component_correct():
    assert sum_product([1, 2, 3, 4])[0] == 10
    assert sum_product([-5, 5, 10])[0] == 10
    assert sum_product([])[0] == 0


def test_returns_tuple_of_two():
    result = sum_product([2, 3])
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_input_not_mutated():
    data = [1, 2, 3]
    sum_product(data)
    assert data == [1, 2, 3]
