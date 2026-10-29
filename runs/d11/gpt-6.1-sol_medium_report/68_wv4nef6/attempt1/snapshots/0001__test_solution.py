import pytest

from solution import fibfib


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 0), (2, 1)])
def test_initial_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n, expected", [(1, 0), (5, 4), (8, 24)])
def test_docstring_examples(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [(3, 1), (4, 2), (6, 7), (7, 13), (9, 44), (10, 81), (12, 274), (15, 1705)],
)
def test_known_sequence_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 11))
def test_recurrence(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)
