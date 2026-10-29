import pytest

from solution import fibfib


def reference_fibfib(n):
    """Iterative reference implementation of the spec in solution.fibfib's docstring."""
    a, b, c = 0, 0, 1
    if n == 0:
        return a
    if n == 1:
        return b
    for _ in range(n - 2):
        a, b, c = b, c, a + b + c
    return c


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 0), (2, 1)])
def test_base_cases(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n, expected", [(1, 0), (5, 4), (8, 24)])
def test_docstring_examples(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [(3, 1), (4, 2), (5, 4), (6, 7), (7, 13), (8, 24), (9, 44), (10, 81), (12, 274), (14, 927)],
)
def test_known_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 20))
def test_recurrence_relation(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)


@pytest.mark.parametrize("n", range(0, 22))
def test_matches_reference(n):
    assert fibfib(n) == reference_fibfib(n)


def test_returns_int():
    assert isinstance(fibfib(10), int)
