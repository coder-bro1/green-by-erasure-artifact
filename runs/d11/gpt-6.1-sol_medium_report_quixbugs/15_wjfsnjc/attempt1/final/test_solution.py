from itertools import permutations
from types import GeneratorType

import pytest

from solution import kheapsort


@pytest.mark.parametrize(
    "arr, k, expected",
    [
        pytest.param([3, 2, 1, 5, 4], 2, [1, 2, 3, 4, 5], id="docstring-example-1"),
        pytest.param([5, 4, 3, 2, 1], 4, [1, 2, 3, 4, 5], id="docstring-example-2"),
        pytest.param([1, 2, 3, 4, 5], 0, [1, 2, 3, 4, 5], id="docstring-example-3"),
        pytest.param([], 0, [], id="empty-zero-k"),
        pytest.param([], 5, [], id="empty-positive-k"),
        pytest.param([42], 0, [42], id="singleton-zero-k"),
        pytest.param([42], 3, [42], id="singleton-large-k"),
        pytest.param([2, 1], 1, [1, 2], id="adjacent-swap"),
        pytest.param([2, 1, 4, 3, 6, 5], 1, [1, 2, 3, 4, 5, 6], id="repeated-swaps"),
        pytest.param([2, 3, 1, 5, 6, 4], 2, [1, 2, 3, 4, 5, 6], id="displaced-minima"),
        pytest.param([3, 1, 2, 6, 4, 5], 2, [1, 2, 3, 4, 5, 6], id="displaced-maxima"),
        pytest.param([-2, -5, 0, 9, 4], 1, [-5, -2, 0, 4, 9], id="mixed-signs"),
        pytest.param([-9, -3, 0, 7], 2, [-9, -3, 0, 7], id="sorted-positive-k"),
        pytest.param([8, -4, 0, 3], 4, [-4, 0, 3, 8], id="k-equals-length"),
        pytest.param([8, -4, 0, 3], 10, [-4, 0, 3, 8], id="k-exceeds-length"),
        pytest.param([10**100, -(10**100), 0], 2, [-(10**100), 0, 10**100], id="large-integers"),
    ],
)
def test_kheapsort_returns_sorted_elements(arr, k, expected):
    assert list(kheapsort(arr, k)) == expected


def test_kheapsort_returns_an_exhaustible_generator():
    result = kheapsort([3, 2, 1, 5, 4], 2)

    assert isinstance(result, GeneratorType)
    assert iter(result) is result
    assert next(result) == 1
    assert list(result) == [2, 3, 4, 5]
    with pytest.raises(StopIteration):
        next(result)


@pytest.mark.parametrize("k", [2, 5, 8])
def test_kheapsort_preserves_input(k):
    arr = [3, 2, 1, 5, 4]
    original = arr.copy()

    result = kheapsort(arr, k)
    assert arr == original
    assert next(result) == 1
    assert arr == original
    assert list(result) == [2, 3, 4, 5]
    assert arr == original


@pytest.mark.parametrize("size", range(7))
def test_kheapsort_all_small_permutations_with_valid_displacements(size):
    expected = list(range(size))
    for permutation in permutations(expected):
        # Values equal their sorted indices, so this is the minimum valid k.
        displacement = max(
            (abs(index - value) for index, value in enumerate(permutation)),
            default=0,
        )
        for k in range(displacement, size + 2):
            arr = list(permutation)
            assert list(kheapsort(arr, k)) == expected, (arr, k)
