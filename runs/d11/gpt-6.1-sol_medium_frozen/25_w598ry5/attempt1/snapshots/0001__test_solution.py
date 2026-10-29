"""Tests for the current implementation, which accepts closing-first pairs.

The implementation's bracket direction differs from its docstring. These tests
record its actual behavior without changing solution.py.
"""

from itertools import product

import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        ("", True),
        (">", False),
        ("<", False),
        ("><", True),
        (">><<", True),
        ("><><", True),
        (">><><<", True),
        ("<>", False),
        ("<<><>>", False),
        (">><", False),
        ("><<", False),
        ("<<<", False),
        (">>>", False),
        ("><<>", False),
        ("<><>", False),
    ],
)
def test_current_bracket_behavior(brackets, expected):
    assert correct_bracketing(brackets) is expected


def test_all_short_strings_against_stack_reference():
    """Check every bracket string of length 0–8 with an independent stack."""
    for length in range(9):
        for characters in product("<>", repeat=length):
            brackets = "".join(characters)
            stack = []
            expected = True
            # Reversal converts the implementation's closing-first convention
            # into the usual opening-first convention for the reference parser.
            for bracket in reversed(brackets):
                if bracket == "<":
                    stack.append(bracket)
                elif stack:
                    stack.pop()
                else:
                    expected = False
                    break
            expected = expected and not stack
            assert correct_bracketing(brackets) is expected, repr(brackets)


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        (">" * 10_000 + "<" * 10_000, True),
        ("><" * 10_000, True),
        (">" * 10_000 + "<" * 9_999, False),
        (">" * 10_000 + "<" * 10_001, False),
        ("<" + "><" * 10_000 + ">", False),
    ],
)
def test_large_inputs(brackets, expected):
    assert correct_bracketing(brackets) is expected
