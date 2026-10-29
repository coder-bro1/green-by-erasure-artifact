"""Tests for the angle-bracket matching contract in solution.py."""

from itertools import product

import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        pytest.param("<", False, id="docstring-unclosed"),
        pytest.param("<>", True, id="docstring-pair"),
        pytest.param("<<><>>", True, id="docstring-nested"),
        pytest.param(">< < >".replace(" ", ""), False, id="docstring-leading-close"),
        pytest.param("", True, id="empty"),
        pytest.param(">", False, id="single-close"),
        pytest.param("<<<<", False, id="only-openings"),
        pytest.param(">>>>", False, id="only-closings"),
        pytest.param("<><><>", True, id="adjacent-pairs"),
        pytest.param("<<<>>>", True, id="deeply-nested"),
        pytest.param("<<>><<>>", True, id="adjacent-nested-groups"),
        pytest.param("<<>", False, id="missing-closing"),
        pytest.param("<>>", False, id="extra-closing"),
        pytest.param("><", False, id="equal-counts-reversed"),
        pytest.param("<>><", False, id="equal-counts-invalid-middle"),
        pytest.param("<<>><", False, id="unclosed-after-valid-group"),
        pytest.param("<<>>>", False, id="extra-close-after-valid-group"),
        pytest.param("<" * 2000 + ">" * 2000, True, id="large-nesting"),
        pytest.param("<>" * 2000, True, id="many-pairs"),
    ],
)
def test_correct_bracketing_examples_and_boundaries(brackets, expected):
    assert correct_bracketing(brackets) is expected


def test_all_short_bracket_strings_against_pair_reduction():
    """Balanced strings reduce to empty by removing adjacent matched pairs."""
    for length in range(11):
        for characters in product("<>", repeat=length):
            brackets = "".join(characters)
            remaining = brackets
            while "<>" in remaining:
                remaining = remaining.replace("<>", "")
            expected = remaining == ""
            assert correct_bracketing(brackets) is expected, repr(brackets)
