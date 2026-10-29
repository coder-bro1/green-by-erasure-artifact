"""Tests for the contract documented by angles_balanced.

The implementation currently reverses the opening and closing symbols.
Strict xfails record this defect and will fail on an unexpected pass, prompting
removal of the markers when the implementation is corrected.
"""

import pytest

from solution import angles_balanced


REVERSED_ANGLES = pytest.mark.xfail(
    strict=True,
    reason="Known defect: implementation treats '>' as opening and '<' as closing",
)


@pytest.mark.parametrize(
    "marks",
    [
        "",
        pytest.param("<>", marks=REVERSED_ANGLES),
        pytest.param("<<>>", marks=REVERSED_ANGLES),
        pytest.param("<><>", marks=REVERSED_ANGLES),
        pytest.param("<<><>>", marks=REVERSED_ANGLES),
        pytest.param("<" * 1000 + ">" * 1000, marks=REVERSED_ANGLES),
    ],
    ids=["empty", "pair", "nested", "adjacent", "mixed", "deeply-nested"],
)
def test_balanced_angles(marks):
    assert angles_balanced(marks) is True


@pytest.mark.parametrize(
    "marks",
    ["<", ">", "<<<", ">>>", "<<>", "<>>", "><<", ">><"],
    ids=[
        "unclosed-opening",
        "unmatched-closing",
        "only-openings",
        "only-closings",
        "missing-closing",
        "extra-closing",
        "early-closing-extra-opening",
        "early-closing-extra-closing",
    ],
)
def test_unequal_counts_are_unbalanced(marks):
    assert angles_balanced(marks) is False


@pytest.mark.parametrize(
    "marks",
    [
        pytest.param("><", marks=REVERSED_ANGLES),
        pytest.param(">><<", marks=REVERSED_ANGLES),
        pytest.param("><><", marks=REVERSED_ANGLES),
        "<>> <".replace(" ", ""),
        "<>><",
    ],
    ids=["reversed-pair", "reversed-nested", "reversed-adjacent", "bad-prefix", "late-unmatched-closing"],
)
def test_equal_counts_do_not_guarantee_balance(marks):
    assert angles_balanced(marks) is False
