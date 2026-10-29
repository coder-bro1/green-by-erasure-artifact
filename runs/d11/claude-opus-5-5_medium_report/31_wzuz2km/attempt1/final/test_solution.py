import pytest

from solution import intersperse

BUG = "solution.py drops the last element of `numbers` (loop over numbers[:-1] never appends numbers[-1])"


def test_empty_list():
    assert intersperse([], 4) == []


def test_empty_list_returns_new_list_object():
    result = intersperse([], 4)
    assert isinstance(result, list)


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_single_element_unchanged():
    assert intersperse([7], 0) == [7]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_two_elements():
    assert intersperse([1, 2], 9) == [1, 9, 2]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_negative_and_zero_values():
    assert intersperse([-1, 0, 5], -3) == [-1, -3, 0, -3, 5]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_delimiter_equal_to_elements():
    assert intersperse([2, 2, 2], 2) == [2, 2, 2, 2, 2]


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("n", [1, 2, 5, 10])
def test_output_length(n):
    assert len(intersperse(list(range(n)), -1)) == 2 * n - 1


@pytest.mark.xfail(strict=True, reason=BUG)
def test_original_elements_preserved_in_order():
    nums = [5, 6, 3, 2]
    assert intersperse(nums, 8)[::2] == nums


def test_delimiters_at_odd_positions():
    # Holds even with the bug: every odd index is the delimiter.
    out = intersperse([5, 6, 3, 2], 8)
    assert all(x == 8 for x in out[1::2])


def test_input_not_mutated():
    nums = [1, 2, 3]
    intersperse(nums, 0)
    assert nums == [1, 2, 3]
