import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    ("weights", "limit", "expected"),
    [
        ([1, 2], 5, False),       # under the limit, but not a palindrome
        ([3, 2, 3], 1, False),    # balanced, but over the limit
        ([3, 2, 3], 9, True),     # balanced and under the limit
        ([3], 5, True),          # a single item is balanced
        ([1, 2, 1], 4, True),     # matching elements around the center
        ([1, 2, 3, 1], 20, False),  # mismatch in an outer pair
        ([2, 1, 1, 2], 6, True),  # even-length palindrome at exact limit
        ([2, 1, 1, 2], 5, False), # balanced, but one over the limit
        ([], 0, True),           # empty list is a palindrome with sum zero
    ],
)
def test_will_it_fly(weights, limit, expected):
    assert will_it_fly(weights, limit) is expected


def test_will_it_fly_does_not_change_input():
    weights = [3, 2, 3]
    original = weights.copy()

    will_it_fly(weights, 8)

    assert weights == original
