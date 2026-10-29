import pytest

from solution import pairs_sum_to_zero


# --- Behaviour that matches the docstring specification ---------------------

@pytest.mark.parametrize(
    "lst, expected",
    [
        ([1, 3, -2, 1], False),
        ([1, 2, 3, 7], False),
        ([2, 4, -5, 3, 5, 7], True),
        ([1], False),
        ([], False),
        ([5, -5], True),
        ([-5, 5], True),
        ([1, 2, 3, -3], True),
        ([-1, -2, -3], False),
        ([1, 2, 3], False),
        ([0, 0], True),  # two distinct zero elements
        ([0, 1, 0], True),
        ([10**12, -(10**12)], True),
        ([3, 3, 3], False),
        ([-4, 1, 2, 4], True),
    ],
)
def test_pairs_sum_to_zero(lst, expected):
    assert pairs_sum_to_zero(lst) is expected


def test_accepts_tuple():
    assert pairs_sum_to_zero((7, -7)) is True
    assert pairs_sum_to_zero((7, 8)) is False


def test_does_not_mutate_input():
    lst = [2, 4, -5, 3, 5, 7]
    copy = list(lst)
    pairs_sum_to_zero(lst)
    assert lst == copy


def test_large_input_without_pair():
    assert pairs_sum_to_zero(list(range(1, 500))) is False


def test_large_input_with_pair_at_end():
    assert pairs_sum_to_zero(list(range(1, 500)) + [-499]) is True


# --- Known bug: an element is paired with itself -----------------------------
# The inner loop starts at j = i, so a single 0 counts as a pair (0 + 0 == 0).
# The docstring requires two *distinct* elements, and its own doctest
# pairs_sum_to_zero([1, 3, 5, 0]) -> False fails. These are strict xfails:
# once solution.py is fixed they will XPASS and fail the run, prompting removal
# of the marker.

@pytest.mark.xfail(strict=True, reason="bug: element paired with itself (j starts at i)")
@pytest.mark.parametrize("lst", [[1, 3, 5, 0], [0], [0, 1, 2]])
def test_single_zero_is_not_a_pair(lst):
    assert pairs_sum_to_zero(lst) is False
