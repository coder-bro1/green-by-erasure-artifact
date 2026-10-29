from itertools import product

import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    "weights, capacity, expected",
    [
        pytest.param([1, 2], 5, False, id="example-unbalanced"),
        pytest.param([3, 2, 3], 1, False, id="example-overweight"),
        pytest.param([3, 2, 3], 9, True, id="example-balanced"),
        pytest.param([3], 5, True, id="example-single-element"),
        pytest.param([3, 2, 3], 8, True, id="exact-capacity"),
        pytest.param([3, 2, 3], 7, False, id="just-over-capacity"),
        pytest.param([3], 3, True, id="single-exact-capacity"),
        pytest.param([3], 2, False, id="single-overweight"),
        pytest.param([], 0, True, id="empty-zero-capacity"),
        pytest.param([], 5, True, id="empty-positive-capacity"),
        pytest.param([], -1, False, id="empty-negative-capacity"),
        pytest.param([0], 0, True, id="single-zero"),
        pytest.param([0, 0, 0], 0, True, id="all-zeros"),
        pytest.param([2, 2], 4, True, id="even-exact-capacity"),
        pytest.param([2, 2], 3, False, id="even-overweight"),
        pytest.param([1, 2, 2, 1], 6, True, id="even-palindrome"),
        pytest.param([1, 2, 4, 2, 1], 10, True, id="odd-palindrome"),
        pytest.param([1, 2, 3, 1], 7, False, id="even-inner-mismatch"),
        pytest.param([1, 2, 0, 3, 1], 7, False, id="odd-inner-mismatch"),
        pytest.param([1, 2, 3], 6, False, id="unbalanced-exact-capacity"),
        pytest.param([1, 2], 0, False, id="unbalanced-and-overweight"),
        pytest.param([-2, 1, -2], -3, True, id="negative-exact-capacity"),
        pytest.param([-2, 1, -2], -4, False, id="negative-overweight"),
        pytest.param([0.5, 1.0, 0.5], 2.0, True, id="fractional-exact-capacity"),
        pytest.param([10**100, 0, 10**100], 2 * 10**100, True, id="large-integers"),
    ],
)
def test_will_it_fly_cases(weights, capacity, expected):
    original = weights.copy()

    assert will_it_fly(weights, capacity) is expected
    assert weights == original


def test_all_short_lists_against_specification():
    for length in range(6):
        for elements in product(range(3), repeat=length):
            weights = list(elements)
            total = sum(weights)
            balanced = weights == weights[::-1]
            for capacity in {-1, 0, total - 1, total, total + 1}:
                expected = balanced and total <= capacity
                assert will_it_fly(weights, capacity) is expected, (
                    f"{weights=}, {capacity=}"
                )
