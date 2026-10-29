"""Tests for powerset, including its known missing-subsets defect."""

import pytest

from solution import powerset


MISSING_SUBSETS = pytest.mark.xfail(
    strict=True,
    reason="Nonempty inputs return only the full set, omitting other subsets.",
)


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        ([], [[]]),
        pytest.param([1], [[], [1]], marks=MISSING_SUBSETS),
        pytest.param([1, 2], [[], [2], [1], [1, 2]], marks=MISSING_SUBSETS),
        pytest.param(
            ["a", "b", "c"],
            [[], ["c"], ["b"], ["b", "c"], ["a"], ["a", "c"],
             ["a", "b"], ["a", "b", "c"]],
            marks=MISSING_SUBSETS,
        ),
    ],
)
def test_documented_subsets_and_order(arr, expected):
    assert powerset(arr) == expected


@pytest.mark.parametrize("size", [1, 2, 3, 5])
@MISSING_SUBSETS
def test_every_subset_is_present_exactly_once(size):
    arr = list(range(size))
    result = powerset(arr)
    expected = {
        tuple(value for index, value in enumerate(arr) if mask & (1 << index))
        for mask in range(1 << size)
    }

    assert len(result) == 2 ** size
    assert {tuple(subset) for subset in result} == expected


@pytest.mark.parametrize("arr", [[], [1], [3, 1, 2], [None, "a", 7], [[1], [2]]])
def test_input_is_unchanged_and_full_subset_is_a_separate_list(arr):
    original = arr.copy()

    result = powerset(arr)

    assert arr == original
    assert isinstance(result, list)
    assert all(isinstance(subset, list) for subset in result)
    assert arr in result
    assert all(subset is not arr for subset in result)
    assert all(
        len({id(subset) for subset in result}) == len(result)
        for _ in [None]
    )


def test_results_are_independent_between_calls():
    first = powerset([])
    first[0].append("changed")
    first.append(["extra"])

    assert powerset([]) == [[]]
