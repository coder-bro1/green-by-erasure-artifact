"""Tests for solution.correct_bracketing, written against its documented spec.

NOTE: solution.py currently has a bug -- the depth counter is inverted
('>' increments, '<' decrements). Tests that expose this are marked
xfail(strict=True): they document the defect, and will turn into hard
failures (XPASS -> error) once the bug is fixed, signalling the markers
should be removed.
"""
import pytest

from solution import correct_bracketing

BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py inverts depth counting ('>' opens, '<' closes)",
)


# --- Cases where the current implementation agrees with the spec -----------

@pytest.mark.parametrize(
    "brackets",
    [
        "<",       # docstring example: unclosed opener
        "><<>",    # docstring example: starts with a closer
        ">",       # lone closer
        "<<<",     # only openers
        ">>>",     # only closers
        "<<>",     # more openers than closers
        "<>>",     # more closers than openers
        "<>><",    # closer goes below zero mid-string
    ],
)
def test_unbalanced_returns_false(brackets):
    assert correct_bracketing(brackets) is False


def test_empty_string_is_balanced():
    assert correct_bracketing("") is True


def test_returns_bool():
    assert isinstance(correct_bracketing("<"), bool)
    assert isinstance(correct_bracketing(""), bool)


# --- Cases that expose the inverted-counter bug ----------------------------

@BUG
@pytest.mark.parametrize(
    "brackets",
    [
        "<>",          # docstring example
        "<<><>>",      # docstring example
        "<><><>",
        "<<<>>>",
        "<<><<>>>",
    ],
)
def test_balanced_returns_true(brackets):
    assert correct_bracketing(brackets) is True


@BUG
@pytest.mark.parametrize("brackets", ["><", "><><", ">><<"])
def test_closer_before_opener_returns_false(brackets):
    assert correct_bracketing(brackets) is False
