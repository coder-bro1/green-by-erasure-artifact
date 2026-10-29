"""Tests for flatten, including its known leaf-value defect."""

from copy import deepcopy
from types import GeneratorType

import pytest

from solution import flatten


@pytest.mark.parametrize("arr", [[], [[]], [[], [[], []]], [[[[[]]]]]])
def test_empty_lists_produce_no_values(arr):
    assert list(flatten(arr)) == []


def test_returns_a_generator():
    result = flatten([1])
    assert isinstance(result, GeneratorType)
    assert iter(result) is result


def test_input_is_not_iterated_until_generator_is_consumed():
    visits = []

    class TrackedList(list):
        def __iter__(self):
            visits.append("iterated")
            return super().__iter__()

    result = flatten(TrackedList([]))
    assert visits == []
    assert list(result) == []
    assert visits == ["iterated"]


def test_does_not_modify_input():
    arr = [1, [], [2, [3]], {"key": [4]}]
    original = deepcopy(arr)
    list(flatten(arr))
    assert arr == original


@pytest.mark.xfail(
    strict=True,
    reason="Known defect: non-list leaves yield flatten(x) instead of x",
)
@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        pytest.param([1, 2, 3], [1, 2, 3], id="flat-list"),
        pytest.param(
            [[1, [], [2, 3]], [[4]], 5],
            [1, 2, 3, 4, 5],
            id="documented-example",
        ),
        pytest.param([[[[7]]]], [7], id="deep-nesting"),
        pytest.param(
            [None, [False, 0, "", b"abc"]],
            [None, False, 0, "", b"abc"],
            id="mixed-leaf-types",
        ),
        pytest.param(
            [[(1, 2)], {"key": [3]}, "text"],
            [(1, 2), {"key": [3]}, "text"],
            id="non-list-containers-remain-leaves",
        ),
    ],
)
def test_flattens_lists_to_leaf_values(arr, expected):
    assert list(flatten(arr)) == expected
