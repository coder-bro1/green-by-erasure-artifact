"""Tests for can_lift's documented palindrome and weight-limit contract."""

from itertools import product

import pytest

from solution import can_lift


MIRROR_BUG = pytest.mark.xfail(
    strict=True,
    reason="can_lift rejects equal mirrored elements instead of unequal ones",
)


@pytest.mark.parametrize(
    "load, limit, expected",
    [
        ([], 0, True),
        ([], 5, True),
        ([], -1, False),
        ([6], 7, True),
        ([6], 6, True),
        ([6], 5, False),
        ([0], 0, True),
        ([-3], -3, True),
        ([-3], -4, False),
        ([4, 1, 4], 8, False),
        ([2, 5], 6, False),
        ([1, 2, 3, 1], 7, False),
        ([1, 2, 3, 1], 20, False),
        ([1, 2, 2, 3], 20, False),
        pytest.param([4, 1, 4], 10, True, marks=MIRROR_BUG),
        pytest.param([4, 1, 4], 9, True, marks=MIRROR_BUG),
        pytest.param([2, 5], 9, False, marks=MIRROR_BUG),
        pytest.param([2, 2], 4, True, marks=MIRROR_BUG),
        pytest.param([1, 2, 2, 1], 6, True, marks=MIRROR_BUG),
        pytest.param([0, 0, 0], 0, True, marks=MIRROR_BUG),
        pytest.param([-2, 1, -2], -3, True, marks=MIRROR_BUG),
        pytest.param([1, 2, 3], 6, False, marks=MIRROR_BUG),
    ],
)
def test_documented_contract(load, limit, expected):
    assert can_lift(load, limit) is expected


def test_over_limit_loads_are_always_rejected():
    """The weight constraint applies regardless of length or symmetry."""
    for length in range(5):
        for values in product((-1, 0, 1), repeat=length):
            load = list(values)
            assert can_lift(load, sum(load) - 1) is False


@pytest.mark.parametrize(
    "load, limit",
    [([], 0), ([6], 7), ([4, 1, 4], 8), ([4, 1, 4], 10), ([2, 5], 9)],
)
def test_does_not_modify_load(load, limit):
    original = load.copy()
    can_lift(load, limit)
    assert load == original
