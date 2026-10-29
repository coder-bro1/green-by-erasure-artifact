"""Tests for the documented behavior of solution.flatten."""

from types import GeneratorType

import pytest

from solution import flatten


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([], [], id="empty-input"),
        pytest.param([[], [[], []], [[[]]]], [], id="nested-empty-lists"),
        pytest.param([1, 2, 3], [1, 2, 3], id="flat-list"),
        pytest.param(
            [[1, [], [2, 3]], [[4]], 5],
            [1, 2, 3, 4, 5],
            id="docstring-example",
        ),
        pytest.param(
            [0, [1, [2], 3], 4, [[5], 6]],
            [0, 1, 2, 3, 4, 5, 6],
            id="preserves-order",
        ),
        pytest.param(
            [1, [1, [2, 1]], 2], [1, 1, 2, 1, 2], id="preserves-duplicates"
        ),
        pytest.param(
            [None, [False, 0, "", [], [True, 1.5]]],
            [None, False, 0, "", True, 1.5],
            id="mixed-and-falsy-values",
        ),
    ],
)
def test_flatten_values(arr, expected):
    assert list(flatten(arr)) == expected


def test_flatten_returns_a_generator():
    result = flatten([[1, 2], 3])

    assert isinstance(result, GeneratorType)
    assert iter(result) is result
    assert next(result) == 1
    assert list(result) == [2, 3]
    with pytest.raises(StopIteration):
        next(result)


def test_non_list_objects_are_yielded_unchanged():
    # Even iterable objects, including those containing lists, remain atomic.
    values = ["abc", b"abc", (1, [2]), {"key": [3]}, {4, 5}, object()]

    result = list(flatten([[value] for value in values]))

    assert len(result) == len(values)
    assert all(actual is expected for actual, expected in zip(result, values))


def test_list_subclasses_are_flattened():
    class ListSubclass(list):
        pass

    assert list(flatten([ListSubclass([1, ListSubclass([2]), []]), 3])) == [1, 2, 3]


def test_shared_nested_list_is_not_a_containment_cycle():
    shared = [1, [2]]

    assert list(flatten([shared, [], shared])) == [1, 2, 1, 2]


def test_flatten_does_not_modify_input():
    inner = [2, []]
    outer = [1, inner, 3]

    assert list(flatten(outer)) == [1, 2, 3]
    assert outer == [1, [2, []], 3]
    assert outer[1] is inner
    assert inner == [2, []]


def test_many_nested_levels():
    arr = ["leaf"]
    for _ in range(100):
        arr = [arr]

    assert list(flatten(arr)) == ["leaf"]
