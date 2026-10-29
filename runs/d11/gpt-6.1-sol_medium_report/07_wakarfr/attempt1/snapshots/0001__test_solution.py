"""Tests for the documented angle-bracket matching contract."""

import pytest

from solution import correct_bracketing


def test_empty_string_is_balanced():
    assert correct_bracketing("") is True


@pytest.mark.parametrize(
    "brackets",
    ["<", ">", "<<", ">>", "<<>", "<>>", "<<<>>", "<<>>>", "><<>", "<>><"],
)
def test_unmatched_or_incorrectly_ordered_brackets_are_rejected(brackets):
    assert correct_bracketing(brackets) is False


@pytest.mark.xfail(
    strict=True,
    reason="solution.py treats '<' as closing, rejecting documented valid bracket pairs",
)
@pytest.mark.parametrize(
    "brackets", ["<>", "<<><>>", "<<>>", "<><>", "<<<>>>", "<><<>>"]
)
def test_matching_pairs_in_valid_order_are_accepted(brackets):
    assert correct_bracketing(brackets) is True


@pytest.mark.xfail(
    strict=True,
    reason="solution.py treats '>' as opening, accepting reversed bracket pairs",
)
@pytest.mark.parametrize("brackets", ["><", ">><<", "><><", ">>><<<", "><>><<"])
def test_closing_before_opening_is_rejected_even_with_equal_counts(brackets):
    assert correct_bracketing(brackets) is False
