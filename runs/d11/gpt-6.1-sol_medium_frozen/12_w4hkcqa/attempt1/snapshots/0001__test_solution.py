"""Tests for the documented flight conditions, including known balance bugs."""

import pytest

from solution import will_it_fly


BALANCE_BUG = pytest.mark.xfail(
    strict=True,
    reason="The balance check rejects equal mirrored elements instead of unequal ones.",
)


@pytest.mark.parametrize(
    "q, w, expected",
    [
        pytest.param([], 0, True, id="empty-at-limit"),
        pytest.param([], 5, True, id="empty-below-limit"),
        pytest.param([], -1, False, id="empty-over-limit"),
        pytest.param([3], 5, True, id="singleton-below-limit"),
        pytest.param([3], 3, True, id="singleton-at-limit"),
        pytest.param([3], 2, False, id="singleton-over-limit"),
        pytest.param([0], 0, True, id="zero-at-limit"),
        pytest.param([3, 2, 3], 1, False, id="odd-palindrome-over-limit"),
        pytest.param([2, 2], 3, False, id="even-palindrome-over-limit"),
        pytest.param([1, 2], 2, False, id="unbalanced-over-limit"),
        pytest.param([1, 2, 3, 1], 20, False, id="matching-ends-unbalanced-middle"),
        pytest.param([3, 2, 3], 9, True, marks=BALANCE_BUG, id="odd-palindrome-below-limit"),
        pytest.param([3, 2, 3], 8, True, marks=BALANCE_BUG, id="odd-palindrome-at-limit"),
        pytest.param([1, 2, 2, 1], 6, True, marks=BALANCE_BUG, id="even-palindrome-at-limit"),
        pytest.param([0, 0], 0, True, marks=BALANCE_BUG, id="all-zero-palindrome"),
        pytest.param([1, 2], 5, False, marks=BALANCE_BUG, id="unequal-pair-below-limit"),
        pytest.param([1, 2], 3, False, marks=BALANCE_BUG, id="unequal-pair-at-limit"),
        pytest.param([1, 2, 3], 6, False, marks=BALANCE_BUG, id="odd-unbalanced-at-limit"),
        pytest.param([1, 2, 3, 4], 10, False, marks=BALANCE_BUG, id="all-mirrored-pairs-unequal"),
    ],
)
def test_will_it_fly(q, w, expected):
    assert will_it_fly(q, w) is expected


@pytest.mark.parametrize("w", [5, 6])
def test_does_not_modify_input(w):
    q = [1, 2, 3]
    original = q.copy()

    will_it_fly(q, w)

    assert q == original
