"""Tests for the powerset contract documented in solution.py."""

from copy import deepcopy

import pytest

from solution import powerset


def test_powerset_of_empty_list():
    assert powerset([]) == [[]]


@pytest.mark.xfail(
    strict=True,
    reason="Nonempty inputs return only the full list, omitting the empty set and proper subsets promised by the docstring.",
)
@pytest.mark.parametrize(
    "arr, expected",
    [
        pytest.param([1], [[], [1]], id="singleton"),
        pytest.param([1, 2], [[], [1], [2], [1, 2]], id="two-elements"),
        pytest.param(
            [1, "a", None],
            [[], [1], ["a"], [None], [1, "a"], [1, None], ["a", None], [1, "a", None]],
            id="mixed-types",
        ),
        pytest.param(
            [[1], [2]],
            [[], [[1]], [[2]], [[1], [2]]],
            id="unhashable-elements",
        ),
    ],
)
def test_powerset_contains_every_subset_exactly_once(arr, expected):
    result = powerset(arr)

    assert isinstance(result, list)
    assert all(isinstance(subset, list) for subset in result)
    # The general contract does not prescribe the order of subsets.
    assert len(result) == len(expected)
    assert all(result.count(subset) == 1 for subset in expected)


@pytest.mark.xfail(
    strict=True,
    reason="The docstring example promises eight subsets, but the implementation returns only [['a', 'b', 'c']].",
)
def test_docstring_example():
    assert powerset(["a", "b", "c"]) == [
        [],
        ["c"],
        ["b"],
        ["b", "c"],
        ["a"],
        ["a", "c"],
        ["a", "b"],
        ["a", "b", "c"],
    ]


@pytest.mark.parametrize("arr", [[], [1, 2, 3], [[1], [2]]])
def test_powerset_does_not_modify_input(arr):
    original = deepcopy(arr)

    powerset(arr)

    assert arr == original
