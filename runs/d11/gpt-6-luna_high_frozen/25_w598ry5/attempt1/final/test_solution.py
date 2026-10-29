import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    ("brackets", "expected"),
    [
        ("", True),
        (">", False),
        ("<", False),
        ("><", True),
        ("<>", False),
        (">><<", True),
        (">><", False),
        ("<>>", False),
        (">><<><", True),
    ],
)
def test_correct_bracketing_current_behavior(brackets, expected):
    """Check empty, balanced, unbalanced, and early-invalid inputs."""
    assert correct_bracketing(brackets) is expected


def test_returns_boolean():
    assert type(correct_bracketing("")) is bool
