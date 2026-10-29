"""Tests for first-occurrence searches, including known missing-value bugs."""

import itertools
from pathlib import Path
import subprocess
import sys

import pytest

from solution import find_first_in_sorted


@pytest.mark.parametrize(
    ("arr", "target", "expected"),
    [
        ([3, 4, 5, 5, 5, 5, 6], 5, 2),
        ([7], 7, 0),
        ([1, 2], 1, 0),
        ([1, 2], 2, 1),
        ([1, 2, 3, 4, 5], 1, 0),
        ([1, 2, 3, 4, 5], 3, 2),
        ([1, 2, 3, 4, 5], 5, 4),
        ([2, 2, 2, 2], 2, 0),
        ([1, 1, 2, 3], 1, 0),
        ([1, 2, 3, 3], 3, 2),
        ([-9, -5, -5, -1, 0, 4], -5, 1),
        ([-2, 0, 0, 0, 2], 0, 1),
        ([-10**100, 0, 10**100, 10**100], 10**100, 2),
    ],
)
def test_returns_first_matching_index(arr, target, expected):
    assert find_first_in_sorted(arr, target) == expected


def test_all_present_values_in_small_sorted_lists():
    """Compare binary search with a linear oracle across duplicate patterns."""
    for length in range(1, 8):
        for values in itertools.combinations_with_replacement(range(-2, 3), length):
            arr = list(values)
            for target in set(arr):
                assert find_first_in_sorted(arr, target) == arr.index(target), (
                    arr,
                    target,
                )


def test_search_does_not_modify_input():
    arr = [-4, -4, 0, 2, 2, 8]
    original = arr.copy()
    for target in set(arr):
        find_first_in_sorted(arr, target)
        assert arr == original


@pytest.mark.xfail(
    strict=True,
    raises=IndexError,
    reason="The upper bound includes len(arr), allowing an out-of-range access.",
)
@pytest.mark.parametrize(
    ("arr", "target"),
    [([], 0), ([1], 2), ([1, 2, 3], 4)],
)
def test_empty_list_or_target_above_maximum_returns_minus_one(arr, target):
    assert find_first_in_sorted(arr, target) == -1


@pytest.mark.xfail(
    strict=True,
    raises=subprocess.TimeoutExpired,
    reason="Setting hi = mid can leave the search bounds unchanged forever.",
)
@pytest.mark.parametrize(
    ("arr", "target"),
    [([1], 0), ([1, 3, 5], 0), ([1, 3, 5], 2), ([1, 3, 5], 4)],
)
def test_missing_target_below_maximum_returns_minus_one(arr, target):
    # Isolate nonterminating searches so they cannot hang the pytest process.
    script = (
        "from solution import find_first_in_sorted; "
        f"print(find_first_in_sorted({arr!r}, {target!r}))"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        timeout=2,
        check=True,
    )
    assert result.stdout.strip() == "-1"
