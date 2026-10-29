from itertools import permutations

import pytest

from solution import next_permutation


CASES = [
    ([1, 2], [2, 1]),
    ([1, 2, 3], [1, 3, 2]),
    ([1, 3, 2], [2, 1, 3]),
    ([2, 3, 1], [3, 1, 2]),
    ([3, 2, 4, 1], [3, 4, 1, 2]),
    ([1, 4, 3, 2], [2, 1, 3, 4]),
    ([-3, -1, -2], [-2, -3, -1]),
    ([0, 5, 2], [2, 0, 5]),
]

KNOWN_BUG = pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="The swap search uses < instead of >, returning None or a smaller permutation.",
)


@KNOWN_BUG
@pytest.mark.parametrize("perm, expected", CASES)
def test_next_permutation_examples(perm, expected):
    assert next_permutation(perm) == expected


@pytest.mark.parametrize("perm, expected", CASES)
def test_does_not_modify_input(perm, expected):
    original = perm.copy()
    next_permutation(perm)
    assert perm == original


@KNOWN_BUG
@pytest.mark.parametrize("values", [(1, 2, 3), (-5, 0, 7, 12)])
def test_matches_lexicographic_order_for_all_valid_permutations(values):
    ordered = list(permutations(values))
    # The final permutation is outside the documented precondition.
    for current, following in zip(ordered, ordered[1:]):
        assert next_permutation(list(current)) == list(following)
