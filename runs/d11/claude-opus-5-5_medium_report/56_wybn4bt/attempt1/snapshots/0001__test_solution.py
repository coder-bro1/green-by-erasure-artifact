import pytest

from solution import add


def test_docstring_example():
    assert add([4, 2, 6, 7]) == 2


@pytest.mark.parametrize(
    "lst, expected",
    [
        ([4, 88], 88),
        ([4, 5, 6, 7, 2, 122], 122),
        ([4, 0, 6, 7], 0),
        ([4, 4, 6, 8], 12),
        ([1, 2, 3, 4, 5, 6], 12),
        ([2, 4, 6, 8, 10, 12, 14], 24),
    ],
)
def test_sums_even_elements_at_odd_indices(lst, expected):
    assert add(lst) == expected


def test_single_element_has_no_odd_index():
    assert add([2]) == 0


def test_even_values_at_even_indices_ignored():
    assert add([2, 1, 4, 3, 6, 5]) == 0


def test_all_odd_values():
    assert add([1, 3, 5, 7, 9]) == 0


def test_negative_even_values():
    assert add([1, -2, 3, -4]) == -6


def test_negative_odd_values_ignored():
    assert add([0, -3, 0, -5]) == 0


def test_does_not_mutate_input():
    lst = [4, 2, 6, 7]
    add(lst)
    assert lst == [4, 2, 6, 7]
