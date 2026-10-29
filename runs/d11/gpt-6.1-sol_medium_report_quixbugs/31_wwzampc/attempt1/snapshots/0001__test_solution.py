import pytest

from solution import find_in_sorted


def test_docstring_example():
    assert find_in_sorted([3, 4, 5, 5, 5, 5, 6], 5) == 3


@pytest.mark.parametrize(
    "arr",
    [
        [0],
        [-5, 5],
        [-10, -3, 0, 4, 12],
        list(range(-10, 10)),
        [7, 7, 7, 7],
        [-3, -3, 0, 0, 0, 5, 5],
    ],
)
def test_present_values_return_a_matching_index(arr):
    for target in set(arr):
        index = find_in_sorted(arr, target)
        assert isinstance(index, int)
        assert 0 <= index < len(arr)
        assert arr[index] == target


@pytest.mark.parametrize("target", [-10, 0, 10])
def test_empty_list_returns_minus_one(target):
    assert find_in_sorted([], target) == -1


@pytest.mark.parametrize(
    "arr, target",
    [([0], -1), ([1, 2], 0), ([-5, -3, 2], -6), ([4, 4, 4], 3)],
)
def test_value_below_minimum_returns_minus_one(arr, target):
    assert find_in_sorted(arr, target) == -1


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The right branch recurses with start=mid rather than mid+1, "
        "so missing values above an examined element cause RecursionError "
        "instead of the documented -1."
    ),
    raises=RecursionError,
)
@pytest.mark.parametrize(
    "arr, target",
    [
        pytest.param([0], 1, id="above-singleton"),
        pytest.param([1, 2, 3], 4, id="above-maximum"),
        pytest.param([2, 2, 2], 3, id="above-duplicates"),
        pytest.param([1, 3], 2, id="gap-in-two-elements"),
        pytest.param([-10, -4, 0, 6, 12], -7, id="negative-gap"),
        pytest.param([-10, -4, 0, 6, 12], 8, id="positive-gap"),
    ],
)
def test_other_missing_values_return_minus_one(arr, target):
    assert find_in_sorted(arr, target) == -1


def test_search_does_not_modify_input():
    arr = [-3, 0, 0, 4, 9]
    original = arr.copy()
    assert arr[find_in_sorted(arr, 4)] == 4
    assert arr == original
