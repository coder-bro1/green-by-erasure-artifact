import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], []),
        ([7], [7]),
        ([1, 2, 3, 2, 3, 4, 2], [1, 2, 3, 3, 3, 4, 4]),
        ([5, 4, 3, 2], [5, 5, 5, 5]),
        ([-8, -3, -6, -2, -10], [-8, -3, -3, -2, -2]),
        ([2, 2, 1, 2, 2], [2, 2, 2, 2, 2]),
        ([0, -1, 4, -5, 3], [0, 0, 4, 4, 4]),
    ],
)
def test_rolling_max(numbers, expected):
    assert rolling_max(numbers) == expected


def test_rolling_max_returns_a_new_list():
    numbers = [1, 3, 2]

    result = rolling_max(numbers)

    assert result == [1, 3, 3]
    assert result is not numbers
    assert numbers == [1, 3, 2]
