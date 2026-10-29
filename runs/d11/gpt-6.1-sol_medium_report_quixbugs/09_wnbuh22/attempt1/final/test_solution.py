from itertools import combinations_with_replacement

import pytest

from solution import find_first_in_sorted


@pytest.mark.parametrize(
    ("arr", "x", "expected"),
    [
        pytest.param([], 0, -1, id="empty"),
        pytest.param([5], 5, 0, id="singleton-found"),
        pytest.param([5], 4, -1, id="singleton-missing-below"),
        pytest.param([5], 6, -1, id="singleton-missing-above"),
        pytest.param([1, 3], 1, 0, id="pair-first"),
        pytest.param([1, 3], 3, 1, id="pair-last"),
        pytest.param([1, 3], 2, -1, id="pair-missing-between"),
        pytest.param([3, 4, 5, 5, 5, 5, 6], 5, 2, id="docstring-example"),
        pytest.param([1, 2, 3, 4, 5], 1, 0, id="first-element"),
        pytest.param([1, 2, 3, 4, 5], 3, 2, id="middle-element"),
        pytest.param([1, 2, 3, 4, 5], 5, 4, id="last-element"),
        pytest.param([1, 2, 3, 4, 5], 0, -1, id="below-minimum"),
        pytest.param([1, 2, 3, 4, 5], 6, -1, id="above-maximum"),
        pytest.param([1, 3, 5, 7], 4, -1, id="missing-interior"),
        pytest.param([2, 2, 2, 3, 4], 2, 0, id="duplicates-at-start"),
        pytest.param([1, 2, 4, 4, 4], 4, 2, id="duplicates-at-end"),
        pytest.param([7, 7, 7, 7], 7, 0, id="all-equal-found"),
        pytest.param([7, 7, 7, 7], 6, -1, id="all-equal-missing-below"),
        pytest.param([7, 7, 7, 7], 8, -1, id="all-equal-missing-above"),
        pytest.param([-8, -5, -5, -1, 0, 3], -5, 1, id="negative-duplicates"),
        pytest.param([-3, 0, 0, 2], 0, 1, id="zero-duplicates"),
        pytest.param(
            [-(10**100), 0, 10**100, 10**100],
            10**100,
            2,
            id="arbitrary-precision-integers",
        ),
    ],
)
def test_find_first_in_sorted_examples(arr, x, expected):
    assert find_first_in_sorted(arr, x) == expected


@pytest.mark.parametrize("length", range(8))
def test_find_first_in_sorted_matches_linear_search(length):
    """Check every sorted list of this length over a small integer domain."""
    for values in combinations_with_replacement(range(-2, 3), length):
        arr = list(values)
        for x in range(-3, 4):
            expected = next((i for i, value in enumerate(arr) if value == x), -1)
            assert find_first_in_sorted(arr, x) == expected, (arr, x, expected)
