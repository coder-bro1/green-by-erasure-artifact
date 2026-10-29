from itertools import product

import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], []),
        ([5], [5]),
        ([-5], [-5]),
        ([0], [0]),
        ([1, 2, 3, 2, 3, 4, 2], [1, 2, 3, 3, 3, 4, 4]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([4, 3, 2, 1], [4, 4, 4, 4]),
        ([3, 3, 3], [3, 3, 3]),
        ([-5, -2, -7, -1], [-5, -2, -2, -1]),
        ([-2, 0, -1, 3, 0], [-2, 0, 0, 3, 3]),
        ([2, 1, 2, 1, 3, 3], [2, 2, 2, 2, 3, 3]),
        ([-10**100, 10**100, 0], [-10**100, 10**100, 10**100]),
    ],
)
def test_rolling_max_examples(numbers, expected):
    assert rolling_max(numbers) == expected


def test_rolling_max_preserves_input_and_returns_new_list():
    numbers = [3, 1, 4, 2]
    original = numbers.copy()

    result = rolling_max(numbers)

    assert numbers == original
    assert result == [3, 3, 4, 4]
    assert result is not numbers


def test_rolling_max_matches_prefix_maxima():
    for length in range(5):
        for values in product((-2, 0, 2), repeat=length):
            numbers = list(values)
            expected = [max(numbers[:end]) for end in range(1, length + 1)]

            assert rolling_max(numbers) == expected, f"Input: {numbers}"
