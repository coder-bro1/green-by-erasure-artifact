import pytest

import solution
from solution import fibfib


def reference(n):
    a, b, c = 0, 0, 1
    for _ in range(n):
        a, b, c = b, c, a + b + c
    return a


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 0), (2, 1)])
def test_base_cases(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n, expected", [(1, 0), (5, 4), (8, 24)])
def test_docstring_examples(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [(3, 1), (4, 2), (6, 7), (7, 13), (9, 44), (10, 81), (11, 149), (12, 274),
     (14, 927), (15, 1705)],
)
def test_known_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 21))
def test_recurrence(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)


@pytest.mark.parametrize("n", range(0, 22))
def test_matches_iterative_reference(n):
    assert fibfib(n) == reference(n)


def test_returns_int():
    assert isinstance(fibfib(10), int)


@pytest.mark.xfail(
    strict=True,
    reason="Docstring asks for an efficient implementation, but solution.py uses "
    "naive triple recursion with no memoization (exponential number of calls).",
)
def test_efficient_call_count(monkeypatch):
    calls = 0
    original = solution.fibfib

    def counting(n):
        nonlocal calls
        calls += 1
        return original(n)

    # Recursive calls resolve the global name `fibfib`, so they hit the wrapper.
    monkeypatch.setattr(solution, "fibfib", counting)
    assert solution.fibfib(20) == reference(20)
    # A linear/memoized implementation needs O(n) calls; allow generous slack.
    assert calls <= 200
