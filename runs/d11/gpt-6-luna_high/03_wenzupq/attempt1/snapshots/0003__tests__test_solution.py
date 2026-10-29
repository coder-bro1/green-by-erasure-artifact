import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
