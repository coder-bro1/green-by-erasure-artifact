import pytest

import solution
from solution import fibfib


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        (1, 0),
        (2, 1),
        (3, 1),
        (4, 2),
        (5, 4),
        (6, 7),
        (7, 13),
        (8, 24),
        (9, 44),
        (10, 81),
        (11, 149),
        (12, 274),
    ],
)
def test_fibfib_sequence_values(n, expected):
    assert fibfib(n) == expected


def test_fibfib_later_value():
    assert fibfib(20) == 35_890


@pytest.mark.xfail(
    strict=True,
    reason="fibfib uses exponential recursion instead of efficiently reusing prior values",
)
def test_fibfib_computes_larger_values_efficiently(monkeypatch):
    original_fibfib = solution.fibfib
    calls = 0

    def counted_fibfib(n):
        nonlocal calls
        calls += 1
        return original_fibfib(n)

    monkeypatch.setattr(solution, "fibfib", counted_fibfib)

    assert solution.fibfib(25) == 755_476
    assert calls <= 3 * 25
