import pytest

from solution import correct_bracketing


@pytest.mark.parametrize(
    "brackets",
    ["", "<>", "<<>>", "<<><>>", "<><><>", "<<<>>>"],
)
def test_correct_bracketing_accepts_balanced_sequences(brackets):
    assert correct_bracketing(brackets) is True


@pytest.mark.parametrize(
    "brackets",
    ["<", ">", "><>", "><<>", "<<>", "<><"],
)
def test_correct_bracketing_rejects_unbalanced_sequences(brackets):
    assert correct_bracketing(brackets) is False
