import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        ("", True),
        ("<>", True),
        ("<<>>", True),
        ("<<><>>", True),
        ("<><><>", True),
        ("<", False),
        (">", False),
        ("<<>", False),
        ("<>>", False),
        ("><<>", False),
        (">><<", False),
    ],
)
def test_correct_bracketing(brackets, expected):
    assert correct_bracketing(brackets) is expected
