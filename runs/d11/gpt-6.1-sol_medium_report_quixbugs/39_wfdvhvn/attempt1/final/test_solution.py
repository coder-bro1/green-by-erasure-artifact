from types import GeneratorType

import pytest

from solution import flatten


@pytest.mark.parametrize("arr", [[], [[]], [[[], [[]]], []]])
def test_empty_lists_produce_no_values(arr):
    assert list(flatten(arr)) == []


def test_returns_a_generator():
    result = flatten([1, [2]])
    assert isinstance(result, GeneratorType)
    assert iter(result) is result


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([[1, [], [2, 3]], [[4]], 5], [1, 2, 3, 4, 5], id="docstring-example"),
        pytest.param([1, 2, 3], [1, 2, 3], id="flat-list"),
        pytest.param([[[[1]]]], [1], id="deep-nesting"),
        pytest.param([[], [1, [], [2]], [], 3], [1, 2, 3], id="order-and-empty-lists"),
        pytest.param([None, False, 0, "", "abc"], [None, False, 0, "", "abc"], id="scalar-leaves"),
        pytest.param([(1, 2), {"key": 3}, {4, 5}, b"ab"], [(1, 2), {"key": 3}, {4, 5}, b"ab"], id="non-list-containers"),
    ],
)
@pytest.mark.xfail(strict=True, reason="flatten yields flatten(x) generators instead of non-list objects")
def test_flattens_to_non_list_objects(arr, expected):
    assert list(flatten(arr)) == expected


@pytest.mark.xfail(strict=True, reason="flatten replaces each non-list object with a generator")
def test_preserves_leaf_identity():
    leaf = object()
    assert list(flatten([[leaf]]))[0] is leaf


@pytest.mark.xfail(strict=True, reason="flatten yields generators instead of the shared lists' leaf values")
def test_shared_lists_are_flattened_each_time_without_mutation():
    shared = [1, [2]]
    arr = [shared, shared]
    result = list(flatten(arr))
    assert arr == [[1, [2]], [1, [2]]]
    assert arr[0] is shared and arr[1] is shared
    assert result == [1, 2, 1, 2]


@pytest.mark.xfail(strict=True, reason="flatten yields generators instead of list subclass leaf values")
def test_list_subclasses_are_flattened():
    class NestedList(list):
        pass

    assert list(flatten([NestedList([1, NestedList([2])])])) == [1, 2]
