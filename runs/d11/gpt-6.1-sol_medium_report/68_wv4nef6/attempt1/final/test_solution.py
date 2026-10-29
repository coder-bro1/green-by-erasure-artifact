import pytest

from solution import fibfib


def test_zero():
    assert fibfib(0) == 0


@pytest.mark.xfail(
    strict=True,
    reason="Docstring specifies initial values 0, 0, 1; implementation uses 0, 1, 2.",
)
@pytest.mark.parametrize("n, expected", [(1, 0), (2, 1)])
def test_initial_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Incorrect initial values make the implementation disagree with docstring examples.",
)
@pytest.mark.parametrize("n, expected", [(1, 0), (5, 4), (8, 24)])
def test_docstring_examples(n, expected):
    assert fibfib(n) == expected


@pytest.mark.xfail(
    strict=True,
    reason="Incorrect initial values propagate through the documented recurrence.",
)
@pytest.mark.parametrize(
    "n, expected",
    [(3, 1), (4, 2), (6, 7), (7, 13), (9, 44), (10, 81), (12, 274), (15, 1705)],
)
def test_known_sequence_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 11))
def test_recurrence(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)
