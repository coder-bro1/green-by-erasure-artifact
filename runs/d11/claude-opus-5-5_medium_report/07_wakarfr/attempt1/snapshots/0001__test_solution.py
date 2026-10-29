import pytest

from solution import correct_bracketing

BUG = ("solution.py swaps the bracket roles: '>' increments depth and '<' "
       "decrements it, so properly nested strings starting with '<' return False")


# Cases where the expected (docstring-specified) result is False.
@pytest.mark.parametrize("s", ["<", "><<>", ">", "<<", ">>", "><", "<>>", "<<>", "<><><<"])
def test_incorrect_bracketing(s):
    assert correct_bracketing(s) is False


def test_empty_string_is_balanced():
    assert correct_bracketing("") is True


# Cases where the expected result is True.
@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("s", ["<>", "<<><>>", "<><>", "<<<>>>", "<<><>><>"])
def test_correct_bracketing(s):
    assert correct_bracketing(s) is True


# Mirror-image strings must NOT be accepted; the buggy code accepts them.
@pytest.mark.xfail(strict=True, reason=BUG)
@pytest.mark.parametrize("s", ["><", ">><<", "><><"])
def test_reversed_strings_rejected(s):
    assert correct_bracketing(s) is False
