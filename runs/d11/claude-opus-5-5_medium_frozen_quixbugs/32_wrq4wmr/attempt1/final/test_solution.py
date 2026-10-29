"""Tests for solution.powerset, written against its documented contract.

KNOWN BUG in solution.py: the recursive branch returns only
``[[first] + s for s in rest_subsets]`` and drops ``rest_subsets`` itself, so
every subset that does not contain the first element is lost (e.g.
``powerset(['a', 'b', 'c']) == [['a', 'b', 'c']]``). The tests that expose this
are marked ``xfail(strict=True)``: they document the intended behaviour and
will start failing loudly (XPASS -> error) once the bug is fixed, signalling
that the markers should be removed.
"""
from itertools import combinations

import pytest

from solution import powerset

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py drops subsets that exclude the first element "
    "(missing `rest_subsets +` in the recursive return)",
)


def as_set_of_frozensets(subsets):
    return {frozenset(s) for s in subsets}


# --- Behaviour that is currently correct -----------------------------------

def test_empty_input_returns_only_empty_set():
    assert powerset([]) == [[]]


@pytest.mark.parametrize("arr", [[1], ["a", "b"], ["a", "b", "c"], list(range(5))])
def test_full_set_is_always_included(arr):
    assert arr in powerset(arr)


@pytest.mark.parametrize("arr", [[1], ["a", "b"], ["a", "b", "c"], list(range(5))])
def test_every_result_is_a_subset_preserving_order(arr):
    for subset in powerset(arr):
        assert set(subset) <= set(arr)
        # Elements appear in the same relative order as in the input.
        assert subset == [x for x in arr if x in subset]


@pytest.mark.parametrize("arr", [[1], ["a", "b"], ["a", "b", "c"], list(range(5))])
def test_no_duplicate_subsets(arr):
    result = powerset(arr)
    assert len(result) == len(as_set_of_frozensets(result))


def test_returns_list_of_lists():
    result = powerset(["x", "y"])
    assert isinstance(result, list)
    assert all(isinstance(s, list) for s in result)


def test_input_is_not_mutated():
    arr = ["a", "b", "c"]
    powerset(arr)
    assert arr == ["a", "b", "c"]


# --- Documented behaviour that fails due to the bug -------------------------

@BUG
def test_docstring_example():
    assert powerset(["a", "b", "c"]) == [
        [], ["c"], ["b"], ["b", "c"], ["a"], ["a", "c"], ["a", "b"], ["a", "b", "c"],
    ]


@BUG
def test_single_element():
    assert powerset([1]) == [[], [1]]


@BUG
@pytest.mark.parametrize("arr", [[1], ["a", "b"], ["a", "b", "c"], list(range(5))])
def test_empty_set_is_always_included(arr):
    assert [] in powerset(arr)


@BUG
@pytest.mark.parametrize("n", [1, 2, 3, 4, 6])
def test_result_has_2_to_the_n_subsets(n):
    assert len(powerset(list(range(n)))) == 2 ** n


@BUG
@pytest.mark.parametrize("arr", [["a", "b"], ["a", "b", "c"], [3, 1, 2, 0]])
def test_matches_itertools_combinations(arr):
    expected = {
        frozenset(c) for r in range(len(arr) + 1) for c in combinations(arr, r)
    }
    assert as_set_of_frozensets(powerset(arr)) == expected
