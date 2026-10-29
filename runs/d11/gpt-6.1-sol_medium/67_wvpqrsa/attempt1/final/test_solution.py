import pytest

from solution import fibfib


@pytest.mark.parametrize(
    ("n", "expected"),
    enumerate([0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927]),
)
def test_initial_sequence(n, expected):
    assert fibfib(n) == expected


@pytest.mark.parametrize("n", range(3, 31))
def test_recurrence(n):
    assert fibfib(n) == fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)


@pytest.mark.parametrize(
    ("n", "expected"),
    [(30, 15902591), (100, 53324762928098149064722658)],
)
def test_larger_inputs(n, expected):
    result = fibfib(n)
    assert isinstance(result, int)
    assert result == expected
