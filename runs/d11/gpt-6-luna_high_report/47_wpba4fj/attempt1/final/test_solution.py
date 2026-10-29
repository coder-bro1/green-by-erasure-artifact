import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        ("<", False),
        ("<>", True),
        ("<<><>>", True),
        ("><<>", False),
    ],
)
def test_docstring_examples(brackets, expected):
    assert correct_bracketing(brackets) is expected


@pytest.mark.parametrize(
    "brackets",
    ["", "<>" * 4, "<<>>", "<<<>>>", "<><><>", "<<><><>>"],
)
def test_balanced_brackets_are_accepted(brackets):
    assert correct_bracketing(brackets) is True


@pytest.mark.parametrize(
    "brackets",
    [">", "><", ">>", "<<>", "<>>", ">><<", "<<><>"],
)
def test_unbalanced_or_prematurely_closed_brackets_are_rejected(brackets):
    assert correct_bracketing(brackets) is False


def test_closing_before_opening_is_rejected_even_if_totals_match():
    assert correct_bracketing("><") is False


def test_all_openings_must_be_closed_at_the_end():
    assert correct_bracketing("<<<>>") is False
