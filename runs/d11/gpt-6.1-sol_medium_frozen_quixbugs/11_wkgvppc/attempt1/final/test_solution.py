"""Tests for bucketsort, including known failures of its sorting contract."""

import pytest

from solution import bucketsort


@pytest.mark.parametrize("k", [0, 1, 5, 100])
def test_empty_input(k):
    assert bucketsort([], k) == []


@pytest.mark.parametrize(
    ("arr", "k", "expected"),
    [
        ([1, 2, 1, 0], 4, [0, 1, 1, 2]),
        ([2, 0, 2, 0], 3, [0, 0, 2, 2]),
        ([2, 0, 2, 0], 4, [0, 0, 2, 2]),
        ([1, 2, 1, 0], 10, [0, 1, 1, 2]),
    ],
)
def test_sorting_when_input_matches_frequency_counts(arr, k, expected):
    # These inputs happen to work despite the known reconstruction bug.
    assert bucketsort(arr, k) == expected


@pytest.mark.parametrize("arr, k", [([], 0), ([0], 1), ([3, 1, 3, 0], 4)])
def test_input_is_not_modified(arr, k):
    original = arr.copy()
    result = bucketsort(arr, k)
    assert arr == original
    assert isinstance(result, list)
    assert result is not arr


def test_results_are_independent_between_calls():
    arr = [1, 2, 1, 0]
    first = bucketsort(arr, 4)
    first.append(99)
    assert bucketsort(arr, 4) == [0, 1, 1, 2]


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: reconstruction enumerates arr instead of counts",
)
@pytest.mark.parametrize(
    "arr, k",
    [
        pytest.param([0], 1, id="single-zero"),
        pytest.param([4], 5, id="single-upper-bound-value"),
        pytest.param([0, 0, 0], 1, id="repeated-zeros"),
        pytest.param([2, 2, 2], 3, id="repeated-positive-value"),
        pytest.param([0, 1, 2, 3], 4, id="already-sorted"),
        pytest.param([3, 2, 1, 0], 4, id="reverse-sorted"),
        pytest.param([4, 0, 2, 4, 1, 0], 5, id="mixed-with-duplicates"),
        pytest.param([9, 0, 9], 10, id="sparse-range"),
    ],
)
def test_documented_sorting_contract(arr, k):
    assert bucketsort(arr, k) == sorted(arr)
