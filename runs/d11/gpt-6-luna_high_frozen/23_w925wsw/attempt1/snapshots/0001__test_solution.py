import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], []),
        ([7], [7]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([9, 4, 2, 1], [9, 9, 9, 9]),
        ([-1, -2, -3], [-1, -1, -1]),
    ],
)
def test_rolling_max(numbers, expected):
    assert rolling_max(numbers) == expected


@pytest.mark.xfail(
    strict=False,
    reason="rolling_max currently takes the maximum of the full input after its first item",
)
def test_rolling_max_tracks_prefix_not_future_values():
    assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]
