import pytest

from solution import intersperse


def test_empty_list():
    assert intersperse([], 4) == []


def test_docstring_example():
    assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]


def test_single_element():
    assert intersperse([7], 0) == [7]


def test_two_elements():
    assert intersperse([5, 6], 8) == [5, 8, 6]


def test_repeated_values():
    assert intersperse([2, 2, 2], 2) == [2, 2, 2, 2, 2]


def test_negative_and_zero_delimiter():
    assert intersperse([1, -1], -5) == [1, -5, -1]
    assert intersperse([3, 4], 0) == [3, 0, 4]


@pytest.mark.parametrize("n", [1, 2, 5, 10])
def test_length_and_structure(n):
    numbers = list(range(n))
    result = intersperse(numbers, -1)
    assert len(result) == 2 * n - 1
    assert result[::2] == numbers
    assert all(x == -1 for x in result[1::2])


def test_input_not_mutated():
    numbers = [1, 2, 3]
    intersperse(numbers, 9)
    assert numbers == [1, 2, 3]


def test_empty_returns_new_list():
    assert intersperse([], 1) is not intersperse([], 1)
