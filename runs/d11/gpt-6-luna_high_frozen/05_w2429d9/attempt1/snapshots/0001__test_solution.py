import pytest

from solution import fibfib


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 6),
        (5, 11),
        (6, 20),
        (7, 37),
        (8, 68),
        (9, 125),
    ],
)
def test_fibfib_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 10))
def test_fibfib_obeys_three_term_recurrence(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)
