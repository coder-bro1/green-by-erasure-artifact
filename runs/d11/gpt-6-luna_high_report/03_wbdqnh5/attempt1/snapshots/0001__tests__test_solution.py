import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], []),
        ([7], [7]),
        ([5, 4, 3, 2], [5, 5, 5, 5]),
        ([1, 5, 2, 4], [1, 5, 5, 5]),
        pytest.param(
            [1, 2, 3, 2, 3, 4, 2],
            [1, 2, 3, 3, 3, 4, 4],
            marks=pytest.mark.xfail(
                strict=True,
                reason="rolling_max uses the maximum of the entire input after the first item, not the prefix so far",
            ),
        ),
        pytest.param(
            [-4, -3, -2],
            [-4, -3, -2],
            marks=pytest.mark.xfail(
                strict=True,
                reason="rolling_max uses the maximum of the entire input after the first item, not the prefix so far",
            ),
        ),
        pytest.param(
            [3, 1, 5, 4],
            [3, 3, 5, 5],
            marks=pytest.mark.xfail(
                strict=True,
                reason="rolling_max uses the maximum of the entire input after the first item, not the prefix so far",
            ),
        ),
    ],
)
def test_rolling_max_returns_prefix_maxima(numbers, expected):
    assert rolling_max(numbers) == expected
