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
def test_flattens_to_non_list_objects(arr, expected):
    assert list(flatten(arr)) == expected


def test_preserves_leaf_identity():
    leaf = object()
    assert list(flatten([[leaf]]))[0] is leaf


def test_shared_lists_are_flattened_each_time_without_mutation():
    shared = [1, [2]]
    arr = [shared, shared]
    result = list(flatten(arr))
    assert arr == [[1, [2]], [1, [2]]]
    assert arr[0] is shared and arr[1] is shared
    assert result == [1, 2, 1, 2]


def test_list_subclasses_are_flattened():
    class NestedList(list):
        pass

    assert list(flatten([NestedList([1, NestedList([2])])])) == [1, 2]
