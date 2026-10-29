import pytest

from solution import will_it_fly


@pytest.mark.parametrize(
    ("q", "weight", "expected"),
    [
        ([1, 2], 5, False),       # Under the limit, but not a palindrome.
        ([3, 2, 3], 1, False),    # A palindrome whose sum is over the limit.
        ([3, 2, 3], 9, True),     # Odd-length palindrome under the limit.
        ([3], 5, True),           # Single element is a palindrome.
        ([1, 2, 2, 1], 6, True),  # Even-length palindrome at the limit.
        ([1, 2, 2, 1], 5, False), # Sum exceeds the limit by one.
        ([1, 2, 3, 1], 100, False),
        ([], 0, True),            # Empty list is symmetric and sums to zero.
        ([-2, 1, -2], -3, True),  # The documented sum condition also applies to negatives.
        ([-2, 1, -2], -4, False),
    ],
)
def test_will_it_fly(q, weight, expected):
    assert will_it_fly(q, weight) is expected
