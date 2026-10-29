"""Tests for solution.tri_sum_seq.

Spec (from the docstring): s(0) = 0, s(1) = 0, s(2) = 1 and
s(k) = s(k-1) + s(k-2) + s(k-3) for k > 2.

NOTE: solution.py currently uses base cases s(1) = 1 and s(2) = 2, which
contradicts the spec. Tests that check spec values the current code gets
wrong are marked xfail(strict=True): they document the bug, and they will
start failing (XPASS -> error) once solution.py is fixed, so the markers
are removed then.
"""
import pytest

from solution import tri_sum_seq

# Reference values computed from the spec: 0, 0, 1, 1, 2, 4, 7, 13, 24, 44, ...
def _reference(k):
    a, b, c = 0, 0, 1
    for _ in range(k):
        a, b, c = b, c, a + b + c
    return a


SPEC_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py uses base cases s(1)=1, s(2)=2 instead of spec s(1)=0, s(2)=1",
)


# --- Tests that hold for the current implementation and the spec alike ---

def test_s0_is_zero():
    assert tri_sum_seq(0) == 0


def test_returns_int():
    assert isinstance(tri_sum_seq(5), int)


@pytest.mark.parametrize("k", range(3, 16))
def test_recurrence_holds(k):
    assert tri_sum_seq(k) == tri_sum_seq(k - 1) + tri_sum_seq(k - 2) + tri_sum_seq(k - 3)


def test_non_decreasing():
    values = [tri_sum_seq(k) for k in range(15)]
    assert values == sorted(values)


def test_reference_helper_matches_known_sequence():
    assert [_reference(k) for k in range(10)] == [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]


# --- Spec conformance (currently failing because of the base-case bug) ---

@SPEC_BUG
def test_s1_is_zero():
    assert tri_sum_seq(1) == 0


@SPEC_BUG
def test_s2_is_one():
    assert tri_sum_seq(2) == 1


@SPEC_BUG
def test_docstring_s6():
    assert tri_sum_seq(6) == 7


@SPEC_BUG
def test_docstring_s9():
    assert tri_sum_seq(9) == 44


@SPEC_BUG
def test_first_values_match_spec():
    assert [tri_sum_seq(k) for k in range(12)] == [_reference(k) for k in range(12)]
