import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], [], id="empty"),
        pytest.param([7], [7], id="single-positive"),
        pytest.param([-7], [-7], id="single-negative"),
        pytest.param([1, 2, 3, 2, 3, 4, 2], [1, 2, 3, 3, 3, 4, 4], id="docstring-example"),
        pytest.param([1, 2, 3, 4], [1, 2, 3, 4], id="increasing"),
        pytest.param([4, 3, 2, 1], [4, 4, 4, 4], id="decreasing"),
        pytest.param([3, 3, 3], [3, 3, 3], id="equal-values"),
        pytest.param([-5, -3, -8, -1], [-5, -3, -3, -1], id="negative-values"),
        pytest.param([-2, 0, -1, 5, 3], [-2, 0, 0, 5, 5], id="mixed-signs"),
        pytest.param([2, 1, 2, 9], [2, 2, 2, 9], id="maximum-at-end"),
    ],
)
def test_rolling_max(numbers, expected):
    assert rolling_max(numbers) == expected


def test_rolling_max_preserves_input_and_returns_new_list():
    numbers = [3, 1, 4, 2]
    original = numbers.copy()

    result = rolling_max(numbers)

    assert numbers == original
    assert result is not numbers
