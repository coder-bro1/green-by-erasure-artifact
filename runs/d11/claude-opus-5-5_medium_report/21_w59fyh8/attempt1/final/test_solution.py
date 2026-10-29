import pytest

from solution import intersperse


def test_empty_list():
    assert intersperse([], 4) == []


def test_docstring_example():
    assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]


def test_single_element_no_delimiter():
    assert intersperse([7], 0) == [7]


def test_two_elements():
    assert intersperse([5, 6], 9) == [5, 9, 6]


@pytest.mark.parametrize(
    "numbers, delim, expected",
    [
        ([2, 2, 2], 2, [2, 2, 2, 2, 2]),
        ([-1, 0, 1], -5, [-1, -5, 0, -5, 1]),
        ([1, 2, 3, 4], 0, [1, 0, 2, 0, 3, 0, 4]),
    ],
)
def test_various(numbers, delim, expected):
    assert intersperse(numbers, delim) == expected


def test_length_property():
    nums = list(range(10))
    out = intersperse(nums, 99)
    assert len(out) == 2 * len(nums) - 1
    assert out[::2] == nums
    assert all(x == 99 for x in out[1::2])


def test_input_not_mutated():
    nums = [1, 2, 3]
    intersperse(nums, 0)
    assert nums == [1, 2, 3]


def test_returns_new_list():
    nums = [1]
    out = intersperse(nums, 0)
    assert out == nums
    assert out is not nums
