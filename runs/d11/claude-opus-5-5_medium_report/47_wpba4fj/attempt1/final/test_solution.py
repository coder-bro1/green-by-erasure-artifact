import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    "brackets, expected",
    [
        # docstring examples
        ("<", False),
        ("<>", True),
        ("<<><>>", True),
        ("><<>", False),
        # edge cases
        ("", True),
        (">", False),
        ("<<", False),
        (">>", False),
        ("><", False),
        ("<><><>", True),
        ("<<<>>>", True),
        ("<<>", False),
        ("<>>", False),
        ("<>><", False),  # balanced count but closes before opening
        ("<<><>><", False),
        ("<<><>>><", False),
        ("<" * 1000 + ">" * 1000, True),
        ("<" * 1000 + ">" * 999, False),
        ("<>" * 500, True),
    ],
)
def test_correct_bracketing(brackets, expected):
    assert correct_bracketing(brackets) is expected


def test_returns_bool():
    assert isinstance(correct_bracketing("<>"), bool)
    assert isinstance(correct_bracketing("><"), bool)
