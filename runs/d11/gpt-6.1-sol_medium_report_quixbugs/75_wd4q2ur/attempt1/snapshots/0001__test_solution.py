"""Tests for the documented next-permutation contract."""

from itertools import permutations

import pytest

from solution import next_permutation


@pytest.mark.parametrize(
    ("perm", "expected"),
    [
        pytest.param([3, 2, 4, 1], [3, 4, 1, 2], id="docstring-example"),
        pytest.param([1, 2], [2, 1], id="two-elements"),
        pytest.param([1, 2, 3, 4], [1, 2, 4, 3], id="ascending"),
        pytest.param([1, 4, 3, 2], [2, 1, 3, 4], id="long-descending-suffix"),
        pytest.param([2, 3, 1], [3, 1, 2], id="pivot-at-start"),
        pytest.param([4, 2, 1, 3], [4, 2, 3, 1], id="pivot-at-end"),
        pytest.param([4, 3, 1, 2], [4, 3, 2, 1], id="last-valid-input"),
        pytest.param([-3, -1, -2], [-2, -3, -1], id="negative-integers"),
        pytest.param([-5, 0, 8, 2], [-5, 2, 0, 8], id="mixed-signs-and-zero"),
        pytest.param([10, 40, 30, 20], [20, 10, 30, 40], id="nonconsecutive-values"),
        pytest.param(
            [0, 10**100, -(10**100)],
            [10**100, -(10**100), 0],
            id="large-integers",
        ),
    ],
)
def test_next_permutation_examples(perm, expected):
    assert next_permutation(perm) == expected


@pytest.mark.parametrize("size", range(2, 7))
def test_every_valid_permutation_has_the_immediate_lexicographic_successor(size):
    # Sorted enumeration gives an independent oracle. The final permutation
    # is excluded because it violates the documented precondition.
    ordered = list(permutations(range(size)))
    for current, successor in zip(ordered, ordered[1:]):
        actual = next_permutation(list(current))
        assert actual == list(successor), f"Incorrect successor for {current}"


def test_input_list_is_preserved_and_result_is_a_list():
    perm = [3, 2, 4, 1]
    original = perm.copy()

    result = next_permutation(perm)

    assert perm == original
    assert isinstance(result, list)
    assert result is not perm
    assert sorted(result) == sorted(original)
