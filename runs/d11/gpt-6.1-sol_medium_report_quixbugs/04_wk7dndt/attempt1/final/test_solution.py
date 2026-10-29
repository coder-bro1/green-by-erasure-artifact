"""Tests for the lowest-index-or-minus-one contract in solution.py."""

from itertools import combinations_with_replacement
from pathlib import Path
import subprocess
import sys

import pytest

from solution import find_first_in_sorted


@pytest.mark.parametrize(
    "arr, target, expected",
    [
        pytest.param([3, 4, 5, 5, 5, 5, 6], 5, 2, id="docstring-example"),
        pytest.param([7], 7, 0, id="singleton"),
        pytest.param([1, 2], 1, 0, id="two-elements-first"),
        pytest.param([1, 2], 2, 1, id="two-elements-last"),
        pytest.param([1, 3, 5, 7, 9], 1, 0, id="first-element"),
        pytest.param([1, 3, 5, 7, 9], 5, 2, id="middle-element"),
        pytest.param([1, 3, 5, 7, 9], 9, 4, id="last-element"),
        pytest.param([2, 2, 2, 3, 4], 2, 0, id="duplicates-at-start"),
        pytest.param([1, 2, 3, 3, 3], 3, 2, id="duplicates-at-end"),
        pytest.param([4, 4, 4, 4], 4, 0, id="all-equal"),
        pytest.param([-9, -5, -5, -1, 0, 3], -5, 1, id="negative-duplicates"),
        pytest.param([-2, 0, 0, 2], 0, 1, id="zero"),
        pytest.param([-(10**100), 0, 10**100], 10**100, 2, id="large-integers"),
    ],
)
def test_returns_lowest_index_for_present_target(arr, target, expected):
    assert find_first_in_sorted(arr, target) == expected


def test_present_targets_across_small_sorted_lists():
    """Compare every present target against an independent linear search."""
    for length in range(1, 7):
        for values in combinations_with_replacement((-2, -1, 0, 1, 2), length):
            arr = list(values)
            for target in set(arr):
                expected = arr.index(target)
                assert find_first_in_sorted(arr, target) == expected, (arr, target)


@pytest.mark.xfail(
    strict=True,
    raises=IndexError,
    reason="hi is len(arr), so empty lists and targets above the maximum index past the list instead of returning -1",
)
@pytest.mark.parametrize(
    "arr, target",
    [
        pytest.param([], 0, id="empty-list"),
        pytest.param([1], 2, id="above-singleton"),
        pytest.param([1, 2, 3], 4, id="above-maximum"),
        pytest.param([-5, -3, -3], -2, id="above-negative-maximum"),
    ],
)
def test_missing_target_returns_minus_one_at_upper_boundary(arr, target):
    assert find_first_in_sorted(arr, target) == -1


@pytest.mark.xfail(
    strict=True,
    reason="hi = mid can leave the search bounds unchanged for absent targets, causing an infinite loop instead of returning -1",
)
@pytest.mark.parametrize(
    "arr, target",
    [
        pytest.param([1], 0, id="below-singleton"),
        pytest.param([1, 2, 3], 0, id="below-minimum"),
        pytest.param([1, 3], 2, id="between-elements"),
        pytest.param([-5, -5, -1, 0, 0, 4], -3, id="gap-with-duplicates"),
    ],
)
def test_missing_target_returns_minus_one_below_or_between_elements(arr, target):
    # Isolate potentially nonterminating calls so pytest can finish and report them.
    script = (
        "from solution import find_first_in_sorted; "
        f"print(find_first_in_sorted({arr!r}, {target!r}))"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=True,
            timeout=2,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Search did not terminate within two seconds; expected -1")
    assert int(result.stdout.strip()) == -1
