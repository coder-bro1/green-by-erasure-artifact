from itertools import permutations

import pytest

from solution import quicksort


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        ([], []),
        ([7], [7]),
        ([1, 2], [1, 2]),
        ([2, 1], [1, 2]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([3, 1, 5, 2, 4], [1, 2, 3, 4, 5]),
        ([-3, -1, -5, -2, -4], [-5, -4, -3, -2, -1]),
        ([0, -2, 3, -1, 2], [-2, -1, 0, 2, 3]),
        ([10**100, 0, -(10**100)], [-(10**100), 0, 10**100]),
    ],
    ids=[
        "empty",
        "singleton",
        "ascending-pair",
        "descending-pair",
        "already-sorted",
        "reverse-sorted",
        "mixed-order",
        "negative-integers",
        "mixed-signs-and-zero",
        "arbitrary-precision-integers",
    ],
)
def test_quicksort_returns_elements_in_sorted_order(arr, expected):
    assert quicksort(arr) == expected


def test_quicksort_all_permutations_of_small_distinct_inputs():
    for length in range(6):
        expected = list(range(length))
        for ordering in permutations(expected):
            assert quicksort(list(ordering)) == expected


@pytest.mark.xfail(
    strict=True,
    reason=(
        "quicksort drops repeated elements: both partitions exclude values "
        "equal to the pivot, violating the documented output of all arr elements"
    ),
)
@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        ([2, 2], [2, 2]),
        ([4, 4, 4, 4], [4, 4, 4, 4]),
        ([0, 0, 0], [0, 0, 0]),
        ([2, 1, 2, 3], [1, 2, 2, 3]),
        ([3, 1, 1, 2], [1, 1, 2, 3]),
        ([1, 3, 2, 3], [1, 2, 3, 3]),
        ([0, -2, 3, -2, 0, 3], [-2, -2, 0, 0, 3, 3]),
    ],
    ids=[
        "equal-pair",
        "all-equal",
        "repeated-zero",
        "repeated-initial-pivot",
        "duplicates-in-lesser-partition",
        "duplicates-in-greater-partition",
        "multiple-repeated-values",
    ],
)
def test_quicksort_preserves_duplicate_elements(arr, expected):
    assert quicksort(arr) == expected
