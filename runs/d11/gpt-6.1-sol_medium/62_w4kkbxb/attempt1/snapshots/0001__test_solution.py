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
        ("><", False),
        ("<<><>>", True),
        ("><<>", False),
        ("<<>>", True),
        ("<><>", True),
        ("<<<>>>", True),
        ("<><<>><>", True),
        ("<<<<", False),
        (">>>>", False),
        ("<<>", False),
        ("<>>", False),
        ("<><", False),
        ("<><>>", False),
        ("<>><", False),
        (">><<", False),
    ],
)
def test_correct_bracketing_examples(brackets, expected):
    assert correct_bracketing(brackets) is expected


@pytest.mark.parametrize("length", range(9))
def test_all_short_bracket_strings(length):
    for characters in product("<>", repeat=length):
        brackets = "".join(characters)
        # A balanced string reduces to empty by removing adjacent pairs.
        remaining = brackets
        while "<>" in remaining:
            remaining = remaining.replace("<>", "")

        assert correct_bracketing(brackets) is (remaining == ""), brackets


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        ("<" * 10_000 + ">" * 10_000, True),
        ("<>" * 10_000, True),
        ("<" * 10_000 + ">" * 9_999, False),
        ("<>" * 10_000 + ">", False),
    ],
    ids=["deep-nesting", "many-pairs", "missing-close", "extra-close"],
)
def test_long_bracket_strings(brackets, expected):
    assert correct_bracketing(brackets) is expected
