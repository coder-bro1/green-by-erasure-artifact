"""Tests for solution.next_permutation.

NOTE: solution.py contains a bug (it must not be modified here). In the inner
loop the comparison is ``perm[j] < perm[i]`` but it should be
``perm[i] < perm[j]`` (find the rightmost element *greater* than the pivot).
Consequently, tests that check the specified behaviour are marked
``xfail(strict=True)``: they document the correct contract and will start
failing loudly (XPASS -> failure) once the bug is fixed, signalling that the
markers and the characterization tests below should be updated.
"""
import itertools

import pytest

from solution import next_permutation

BUG = "solution.py compares perm[j] < perm[i]; should be perm[i] < perm[j]"


def reference_next_permutation(perm):
    """Correct reference: next permutation in lexicographic order."""
    perms = sorted(itertools.permutations(sorted(perm)))
    idx = perms.index(tuple(perm))
    return list(perms[idx + 1])


def all_non_last_permutations(max_n=5):
    cases = []
    for n in range(2, max_n + 1):
        for p in itertools.permutations(range(n)):
            if list(p) != sorted(p, reverse=True):
                cases.append(list(p))
    return cases


# ---------------------------------------------------------------------------
# Specification tests (expected to fail because of the bug in solution.py)
# ---------------------------------------------------------------------------

@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    assert next_permutation([3, 2, 4, 1]) == [3, 4, 1, 2]


@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize(
    "perm, expected",
    [
        ([0, 1], [1, 0]),
        ([1, 2, 3], [1, 3, 2]),
        ([1, 3, 2], [2, 1, 3]),
        ([2, 1, 3], [2, 3, 1]),
        ([2, 3, 1], [3, 1, 2]),
        ([3, 1, 2], [3, 2, 1]),
        ([3, 5, 6, 2, 1], [3, 6, 1, 2, 5]),
        ([3, 5, 6, 2], [3, 6, 2, 5]),
        ([4, 5, 1, 7, 9], [4, 5, 1, 9, 7]),
        ([4, 5, 8, 7, 1], [4, 7, 1, 5, 8]),
        ([9, 5, 2, 6, 1], [9, 5, 6, 1, 2]),
        ([44, 5, 1, 7, 9], [44, 5, 1, 9, 7]),
        ([-3, -1, -2], [-2, -3, -1]),
    ],
)
def test_known_cases(perm, expected):
    assert next_permutation(perm) == expected


@pytest.mark.xfail(strict=True, reason=BUG)
def test_matches_reference_exhaustively():
    for perm in all_non_last_permutations():
        assert next_permutation(perm) == reference_next_permutation(perm), perm


@pytest.mark.xfail(strict=True, reason=BUG)
def test_iterating_walks_all_permutations_in_order():
    perm = [0, 1, 2, 3]
    seen = [perm]
    while perm != [3, 2, 1, 0]:
        perm = next_permutation(perm)
        seen.append(perm)
    assert seen == [list(p) for p in itertools.permutations(range(4))]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_result_is_lexicographically_greater():
    for perm in all_non_last_permutations(4):
        assert next_permutation(perm) > perm, perm


# ---------------------------------------------------------------------------
# Properties that hold for the current implementation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("perm", all_non_last_permutations())
def test_does_not_mutate_input(perm):
    original = list(perm)
    next_permutation(perm)
    assert perm == original


@pytest.mark.parametrize("perm", all_non_last_permutations())
def test_result_when_returned_is_new_list_with_same_elements(perm):
    result = next_permutation(perm)
    if result is not None:
        assert result is not perm
        assert sorted(result) == sorted(perm)


def test_accepts_tuple_input_without_error():
    # list(perm) copy means tuples are accepted
    assert next_permutation((1, 2, 0)) == [0, 1, 2]


# ---------------------------------------------------------------------------
# Characterization tests: pin down current (buggy) behaviour
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "perm, actual",
    [
        ([3, 2, 4, 1], [3, 1, 2, 4]),   # correct answer: [3, 4, 1, 2]
        ([1, 2, 0], [0, 1, 2]),         # correct answer: [2, 0, 1]
        ([0, 1], None),                 # correct answer: [1, 0]
        ([0, 1, 2], None),              # correct answer: [0, 2, 1]
        ([0, 2, 1], None),              # correct answer: [1, 0, 2]
        ([1, 0, 2], None),              # correct answer: [1, 2, 0]
        ([2, 0, 1], None),              # correct answer: [2, 1, 0]
    ],
)
def test_current_buggy_behaviour(perm, actual):
    assert next_permutation(perm) == actual


def test_reverse_sorted_input_returns_none():
    # Outside the precondition: no next permutation exists.
    assert next_permutation([2, 1, 0]) is None


def test_reference_helper_is_correct():
    assert reference_next_permutation([3, 2, 4, 1]) == [3, 4, 1, 2]
    assert reference_next_permutation([1, 2, 3]) == [1, 3, 2]
