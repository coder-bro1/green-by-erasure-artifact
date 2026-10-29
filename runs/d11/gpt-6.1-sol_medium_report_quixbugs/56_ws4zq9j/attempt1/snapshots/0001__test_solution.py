"""Tests for the documented contract of solution.lis (unique integers)."""

import pytest

from solution import lis


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([7], 1, id="singleton"),
        pytest.param([1, 2, 3, 4, 5], 5, id="increasing"),
        pytest.param([5, 4, 3, 2, 1], 1, id="decreasing"),
        pytest.param([1, 2], 2, id="increasing-pair"),
        pytest.param([2, 1], 1, id="decreasing-pair"),
        pytest.param([-5, -3, -1], 3, id="negative-increasing"),
        pytest.param([-1, -3, -5], 1, id="negative-decreasing"),
        pytest.param([-4, 0, -2, 3, 1, 5], 4, id="mixed-signs"),
        pytest.param([3, 1, 2], 2, id="skip-initial-value"),
        pytest.param([1, 3, 2, 4], 3, id="subsequence-is-not-contiguous"),
        pytest.param([2, 5, 3, 4, 6], 4, id="replace-subsequence-tail"),
        pytest.param([10**100, -(10**100), 0, 10**99], 3, id="large-integers"),
        pytest.param((), 0, id="empty-tuple"),
        pytest.param((3, 1, 2, 4), 3, id="tuple"),
        pytest.param(range(-3, 4), 7, id="increasing-range"),
        pytest.param(range(4, -3, -1), 1, id="decreasing-range"),
    ],
)
def test_lis_documented_inputs(values, expected):
    assert lis(values) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Updating a shorter subsequence overwrites longest; the docstring example returns 2 instead of 3.",
)
def test_lis_docstring_example():
    assert lis([4, 1, 5, 3, 7, 6, 2]) == 3


@pytest.mark.xfail(
    strict=True,
    reason="A trailing minimum resets longest to 1 even though an increasing subsequence of length 2 exists.",
)
def test_lis_preserves_longest_after_trailing_minimum():
    assert lis([1, 2, 0]) == 2


@pytest.mark.xfail(
    strict=True,
    reason="Replacing a shorter tail reduces longest from 3 to 2, losing an existing subsequence.",
)
def test_lis_preserves_longest_after_shorter_tail_update():
    assert lis([0, 2, 3, 1]) == 3


@pytest.mark.xfail(
    strict=True,
    reason="After longest shrinks, later values cannot extend the previously recorded longest subsequence.",
)
def test_lis_extends_previous_longest_after_new_minimum():
    assert lis([1, 2, 0, 3]) == 3


def test_lis_does_not_modify_input():
    values = [2, 5, 3, 4, 6]
    original = values.copy()

    assert lis(values) == 4
    assert values == original
