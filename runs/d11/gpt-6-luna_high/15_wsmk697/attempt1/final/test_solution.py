import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    ("items", "max_weight", "expected"),
    [
        ([1, 2], 5, False),       # Within the weight limit, but not balanced.
        ([3, 2, 3], 5, False),    # Balanced, but too heavy.
        ([3, 2, 3], 8, True),     # Balanced and exactly at the limit.
        ([3, 2, 3], 9, True),     # Balanced and under the limit.
        ([3], 3, True),           # A single-item list is a palindrome.
        ([], 0, True),            # An empty list is balanced and weighs zero.
        ([1, 2, 1], 4, True),     # Odd-length palindrome.
        ([1, 2, 2, 1], 6, True),  # Even-length palindrome.
        ([1, 2, 3, 1], 7, False), # Same total weight, but not a palindrome.
    ],
)
def test_will_it_fly(items, max_weight, expected):
    assert will_it_fly(items, max_weight) is expected


def test_will_it_fly_returns_false_when_empty_list_exceeds_limit():
    assert will_it_fly([], -1) is False

