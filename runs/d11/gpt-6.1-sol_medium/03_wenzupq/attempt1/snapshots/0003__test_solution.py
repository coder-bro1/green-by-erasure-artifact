from itertools import product

import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        ("", True),
        ("<", False),
        (">", False),
        ("<>", True),
        ("<<><>>", True),
        ("><<>", False),
        ("<<<<", False),
        (">>>>", False),
        ("<<<<>>>>", True),
        ("<><><>", True),
        ("<><<>>", True),
        ("><", False),
        ("<>>", False),
        ("<<>", False),
        ("<>>><<", False),
        ("<><", False),
    ],
)
def test_correct_bracketing_examples_and_edge_cases(brackets, expected):
    assert correct_bracketing(brackets) is expected


def test_all_short_bracket_strings():
    # Valid bracket strings reduce to empty by removing matched adjacent pairs.
    for length in range(11):
        for characters in product("<>", repeat=length):
            brackets = "".join(characters)
            reduced = brackets
            while "<>" in reduced:
                reduced = reduced.replace("<>", "")
            assert correct_bracketing(brackets) is (reduced == ""), brackets


@pytest.mark.parametrize(
    "brackets",
    ["<>" * 10_000, "<" * 10_000 + ">" * 10_000],
    ids=["repeated-pairs", "deeply-nested"],
)
def test_long_valid_bracket_strings(brackets):
    assert correct_bracketing(brackets) is True
