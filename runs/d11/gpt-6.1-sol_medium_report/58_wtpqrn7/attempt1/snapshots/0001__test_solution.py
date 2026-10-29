from itertools import product

import pytest

from solution import rolling_max


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], [], id="empty"),
        pytest.param([5], [5], id="single-positive"),
        pytest.param([-5], [-5], id="single-negative"),
        pytest.param([0], [0], id="single-zero"),
        pytest.param(
            [1, 2, 3, 2, 3, 4, 2],
            [1, 2, 3, 3, 3, 4, 4],
            id="docstring-example",
        ),
        pytest.param([1, 2, 3, 4], [1, 2, 3, 4], id="increasing"),
        pytest.param([4, 3, 2, 1], [4, 4, 4, 4], id="decreasing"),
        pytest.param([2, 2, 2], [2, 2, 2], id="equal-values"),
        pytest.param([-5, -2, -8, -1], [-5, -2, -2, -1], id="all-negative"),
        pytest.param([-3, 0, -1, 2, -4], [-3, 0, 0, 2, 2], id="mixed-signs"),
        pytest.param([0, 0, -1, 0], [0, 0, 0, 0], id="zero-maximum"),
        pytest.param([5, 1, 5, 2, 6, 6], [5, 5, 5, 5, 6, 6], id="repeated-maxima"),
        pytest.param(
            [-(10**100), 10**100, 10**100 - 1],
            [-(10**100), 10**100, 10**100],
            id="large-integers",
        ),
    ],
)
def test_rolling_max_examples(numbers, expected):
    assert rolling_max(numbers) == expected


@pytest.mark.parametrize("length", range(6))
def test_rolling_max_matches_each_prefix_maximum(length):
    for values in product((-2, -1, 0, 1, 2), repeat=length):
        numbers = list(values)
        expected = [max(numbers[:end]) for end in range(1, length + 1)]
        assert rolling_max(numbers) == expected, f"Input: {numbers!r}"


def test_rolling_max_calls_are_independent():
    assert rolling_max([100, 1]) == [100, 100]
    assert rolling_max([-3, -2]) == [-3, -2]
    assert rolling_max([]) == []
    assert rolling_max([0, 1]) == [0, 1]
