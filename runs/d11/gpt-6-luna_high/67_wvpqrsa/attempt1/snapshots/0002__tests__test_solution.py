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
        (20, 35890),
    ],
)
def test_fibfib_known_values(n, expected):
    assert fibfib(n) == expected


def test_fibfib_computes_large_indices_iteratively():
    # This index is too large for a recursive implementation to handle
    # efficiently, while remaining quick for an iterative implementation.
    assert fibfib(1000) > fibfib(999) > 0


@pytest.mark.parametrize("n", [-1, -10])
def test_fibfib_rejects_negative_indices(n):
    with pytest.raises(ValueError, match="non-negative"):
        fibfib(n)
