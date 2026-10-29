import pytest
from solution import angles_balanced


@pytest.mark.parametrize("marks", ["", "<>", "<<>>", "<><>", "<<><>>", "<" * 50 + ">" * 50])
def test_balanced(marks):
    assert angles_balanced(marks) is True


@pytest.mark.parametrize("marks", ["<", ">", "><", "<<>", "<>>", "><<>", "<>><", ">>><<<"])
def test_unbalanced(marks):
    assert angles_balanced(marks) is False


def test_docstring_examples():
    assert angles_balanced('<<>>') is True
    assert angles_balanced('><') is False
    assert angles_balanced('<') is False
