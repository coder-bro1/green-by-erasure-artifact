from itertools import combinations, product

import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    "numbers, expected",
    [
        pytest.param([], False, id="empty"),
        pytest.param([1], False, id="single-positive"),
        pytest.param([-1], False, id="single-negative"),
        pytest.param([0], False, id="single-zero-cannot-pair-with-itself"),
        pytest.param([1, 3, 5, 0], False, id="docstring-single-zero"),
        pytest.param([1, 3, -2, 1], False, id="docstring-mixed-signs"),
        pytest.param([1, 2, 3, 7], False, id="docstring-all-positive"),
        pytest.param([2, 4, -5, 3, 5, 7], True, id="docstring-pair"),
        pytest.param([-1, -2, -3], False, id="all-negative"),
        pytest.param([2, 2], False, id="equal-nonzero-values"),
        pytest.param([0, 0], True, id="two-distinct-zero-positions"),
        pytest.param([7, -7], True, id="positive-before-negative"),
        pytest.param([-7, 7], True, id="negative-before-positive"),
        pytest.param([5, 2, 3, -5], True, id="pair-at-opposite-ends"),
        pytest.param([8, 2, -2], True, id="pair-at-end"),
        pytest.param([3, 3, -3], True, id="duplicate-with-opposite"),
        pytest.param([0, 2, 2, -3], False, id="zero-and-unmatched-duplicates"),
        pytest.param([10**100, -(10**100)], True, id="large-integers"),
        pytest.param([10**100, -(10**100) + 1], False, id="large-near-opposites"),
    ],
)
def test_pairs_sum_to_zero(numbers, expected):
    original = numbers.copy()

    assert pairs_sum_to_zero(numbers) is expected
    assert numbers == original


def test_pairs_sum_to_zero_exhaustive_small_lists():
    """Compare every short list with a distinct-position pair oracle."""
    for length in range(6):
        for values in product(range(-2, 3), repeat=length):
            numbers = list(values)
            expected = any(a + b == 0 for a, b in combinations(numbers, 2))

            assert pairs_sum_to_zero(numbers) is expected, numbers
