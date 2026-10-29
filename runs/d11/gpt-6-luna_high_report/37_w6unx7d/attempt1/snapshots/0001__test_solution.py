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
        (11, 149),
        (12, 274),
    ],
)
def test_fibfib_sequence_values(n, expected):
    assert fibfib(n) == expected


def test_fibfib_later_value():
    assert fibfib(20) == 35_890
