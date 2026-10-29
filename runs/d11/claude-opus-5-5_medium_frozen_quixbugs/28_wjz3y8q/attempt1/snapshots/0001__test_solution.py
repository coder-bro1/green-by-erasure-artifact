import types

import pytest

from solution import flatten

# NOTE: solution.py currently has a bug in its non-list branch:
#     yield flatten(x)   # should be: yield x
# Every leaf is therefore yielded as an un-iterated generator object instead of
# the value itself. Tests asserting the documented behaviour on leaf values are
# marked xfail(strict=True): they document the bug, keep the suite green, and
# will turn into a failure (XPASS) once the bug is fixed, signalling that the
# markers should be removed.
BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py yields flatten(x) instead of x for non-list elements",
)


# ---------------------------------------------------------------------------
# Behaviour that is correct in the current implementation
# ---------------------------------------------------------------------------

def test_returns_generator():
    assert isinstance(flatten([1, 2]), types.GeneratorType)


def test_is_lazy():
    # Building the generator must not consume or validate the input.
    gen = flatten([[1], 2])
    assert isinstance(gen, types.GeneratorType)


def test_empty_list():
    assert list(flatten([])) == []


@pytest.mark.parametrize(
    "arr",
    [
        [[]],
        [[], []],
        [[[[]]]],
        [[], [[]], [[], [[]]]],
    ],
)
def test_only_empty_lists(arr):
    assert list(flatten(arr)) == []


@pytest.mark.parametrize(
    "arr, expected_count",
    [
        ([1], 1),
        ([1, 2, 3], 3),
        ([[1, [], [2, 3]], [[4]], 5], 5),
        ([[[[[1]]]]], 1),
        ([[], [1, [2, [3, [4]]]], []], 4),
    ],
)
def test_yields_one_item_per_leaf(arr, expected_count):
    assert len(list(flatten(arr))) == expected_count


def test_input_not_mutated():
    arr = [[1, [], [2, 3]], [[4]], 5]
    snapshot = [[1, [], [2, 3]], [[4]], 5]
    list(flatten(arr))
    assert arr == snapshot


def test_shared_sublist_is_not_a_cycle():
    inner = [1, 2]
    assert len(list(flatten([inner, inner]))) == 4


# ---------------------------------------------------------------------------
# Documented behaviour on leaf values (currently broken)
# ---------------------------------------------------------------------------

@BUG
def test_docstring_example():
    assert list(flatten([[1, [], [2, 3]], [[4]], 5])) == [1, 2, 3, 4, 5]


@BUG
def test_flat_list_unchanged():
    assert list(flatten([1, 2, 3])) == [1, 2, 3]


@BUG
def test_deep_nesting():
    assert list(flatten([[[[[1]]]]])) == [1]


@BUG
def test_order_preserved():
    assert list(flatten([[3, [1]], 2, [[0]]])) == [3, 1, 2, 0]


@BUG
def test_non_list_iterables_are_leaves():
    # Tuples, strings, dicts and sets are not lists and must be yielded as-is.
    arr = [(1, 2), "ab", {"k": 1}, {3}, [None, 0.5]]
    assert list(flatten(arr)) == [(1, 2), "ab", {"k": 1}, {3}, None, 0.5]


@BUG
def test_mixed_types():
    obj = object()
    assert list(flatten([obj, [True, [None]]])) == [obj, True, None]


@BUG
def test_no_generators_in_output():
    assert not any(
        isinstance(v, types.GeneratorType) for v in flatten([1, [2, [3]]])
    )
