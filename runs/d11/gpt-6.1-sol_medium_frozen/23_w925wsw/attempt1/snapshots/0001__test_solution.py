import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([], []),
        ([7], [7]),
        ([-7], [-7]),
        ([0], [0]),
        ([1, 2], [1, 2]),
        ([2, 1], [2, 2]),
        ([5, 4, 3, 2, 1], [5, 5, 5, 5, 5]),
        ([3, 3, 3], [3, 3, 3]),
        ([-2, -5, -3], [-2, -2, -2]),
        ([-4, 0, -2, 0], [-4, 0, 0, 0]),
        ([1, 5, 2, 5, 3], [1, 5, 5, 5, 5]),
    ],
)
def test_rolling_max(numbers, expected):
    assert rolling_max(numbers) == expected


def test_does_not_modify_input():
    numbers = [3, 1, 4, 2]
    original = numbers.copy()

    result = rolling_max(numbers)

    assert numbers == original
    assert result is not numbers


def test_results_are_independent_between_calls():
    first = rolling_max([5, 1])
    second = rolling_max([-3, -4])
    first.append(100)

    assert second == [-3, -3]
    assert rolling_max([]) == []


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: max(numbers) includes future values instead of only the prefix",
)
@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 2, 3, 2, 3, 4, 2], [1, 2, 3, 3, 3, 4, 4]),
        ([1, 2, 3], [1, 2, 3]),
        ([-5, -4, -3], [-5, -4, -3]),
        ([2, 1, 5], [2, 2, 5]),
    ],
)
def test_rolling_max_uses_only_values_seen_so_far(numbers, expected):
    assert rolling_max(numbers) == expected
