"""Tests for solution.find_first_in_sorted.

Cases where the value is present test the documented behaviour directly.
Cases where the value is absent (or the list is empty) hit known bugs in
solution.py (IndexError or an infinite loop). They are marked strict xfail
and run in a subprocess with a timeout, so a hang cannot stall the suite.
If solution.py is fixed, these will XPASS and fail strictly, signalling that
the markers should be removed.
"""
import bisect
import multiprocessing as mp
import random

import pytest

from solution import find_first_in_sorted

TIMEOUT = 2.0


def _reference(arr, x):
    i = bisect.bisect_left(arr, x)
    return i if i < len(arr) and arr[i] == x else -1


def _worker(arr, x, q):
    try:
        q.put(("ok", find_first_in_sorted(arr, x)))
    except Exception as e:  # pragma: no cover - reported to parent
        q.put(("err", repr(e)))


def call_with_timeout(arr, x, timeout=TIMEOUT):
    q = mp.Queue()
    p = mp.Process(target=_worker, args=(arr, x, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        raise TimeoutError(f"find_first_in_sorted({arr!r}, {x!r}) did not terminate")
    status, value = q.get(timeout=1)
    if status == "err":
        raise RuntimeError(value)
    return value


# ---------- value present: documented behaviour ----------

def test_docstring_example():
    assert find_first_in_sorted([3, 4, 5, 5, 5, 5, 6], 5) == 2


@pytest.mark.parametrize(
    "arr, x, expected",
    [
        ([1], 1, 0),
        ([1, 2, 3, 4, 5], 1, 0),
        ([1, 2, 3, 4, 5], 3, 2),
        ([1, 2, 3, 4, 5], 5, 4),
        ([2, 2, 2, 2], 2, 0),
        ([1, 1, 2, 2, 3, 3], 3, 4),
        ([1, 2, 2, 2, 2, 2, 2, 3], 2, 1),
        ([0, 0, 0, 7], 7, 3),
        ([-5, -3, -3, 0, 4], -3, 1),
        ([-5, -3, -3, 0, 4], -5, 0),
    ],
)
def test_present_returns_first_index(arr, x, expected):
    assert find_first_in_sorted(arr, x) == expected


def test_does_not_mutate_input():
    arr = [1, 2, 2, 3]
    find_first_in_sorted(arr, 2)
    assert arr == [1, 2, 2, 3]


def test_randomized_present_values_match_reference():
    rng = random.Random(12345)
    for _ in range(500):
        arr = sorted(rng.randint(-20, 20) for _ in range(rng.randint(1, 40)))
        x = rng.choice(arr)
        result = find_first_in_sorted(arr, x)
        assert result == _reference(arr, x)
        assert arr[result] == x
        assert result == 0 or arr[result - 1] != x


# ---------- value absent: known bugs in solution.py ----------

@pytest.mark.xfail(strict=True, reason="bug: IndexError on empty list (hi=len(arr), lo<=hi)")
def test_empty_list_returns_minus_one():
    assert call_with_timeout([], 1) == -1


@pytest.mark.xfail(strict=True, reason="bug: IndexError when x is greater than all elements")
def test_absent_greater_than_all():
    assert call_with_timeout([1, 2, 3], 10) == -1


@pytest.mark.xfail(strict=True, reason="bug: infinite loop when x is smaller than all elements")
def test_absent_smaller_than_all():
    assert call_with_timeout([5, 6, 7], 1) == -1


@pytest.mark.xfail(strict=True, reason="bug: infinite loop when x falls in a gap")
def test_absent_in_gap():
    assert call_with_timeout([1, 3], 2) == -1
