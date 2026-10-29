import pytest

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
        (15, 1705),
        (20, 35890),
    ],
)
def test_fibfib_known_values(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 16))
def test_fibfib_recurrence(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)


def test_fibfib_repeated_calls_are_independent():
    inputs = [8, 0, 5, 2, 8, 1, 5]
    assert [fibfib(n) for n in inputs] == [24, 0, 4, 1, 24, 0, 4]
