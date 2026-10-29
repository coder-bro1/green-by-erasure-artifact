from itertools import product

import pytest

from solution import quicksort


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([], [], id="empty"),
        pytest.param([7], [7], id="single-element"),
        pytest.param([2, 1], [1, 2], id="two-reversed-elements"),
        pytest.param([1, 2, 3, 4], [1, 2, 3, 4], id="already-sorted"),
        pytest.param([4, 3, 2, 1], [1, 2, 3, 4], id="reverse-sorted"),
        pytest.param([3, 1, 4, 2], [1, 2, 3, 4], id="mixed-order"),
        pytest.param([5, 5, 5, 5], [5, 5, 5, 5], id="all-equal"),
        pytest.param([3, 1, 3, 2, 1], [1, 1, 2, 3, 3], id="duplicates"),
        pytest.param([-2, -5, -1, -3], [-5, -3, -2, -1], id="negative-integers"),
        pytest.param([0, -2, 3, 0, -1], [-2, -1, 0, 0, 3], id="mixed-signs"),
        pytest.param(
            [10**100, 0, -(10**100), 1, -1],
            [-(10**100), -1, 0, 1, 10**100],
            id="arbitrary-precision-integers",
        ),
    ],
)
def test_quicksort_returns_elements_in_sorted_order(arr, expected):
    assert quicksort(arr) == expected


def test_quicksort_matches_sorted_for_all_small_integer_lists():
    # Exhaustively cover pivot positions, repeated values, and mixed signs.
    for length in range(5):
        for values in product(range(-2, 3), repeat=length):
            arr = list(values)
            assert quicksort(arr) == sorted(arr), f"Failed for input {arr!r}"
