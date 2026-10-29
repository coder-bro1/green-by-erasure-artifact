import pytest

from solution import add


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([4, 2, 6, 7], 2),  # Example from the docstring.
        ([1, 4, 3, 8, 5, 10], 22),  # Even values at indices 1, 3, and 5.
        ([2], 0),  # The only value is at an even index.
        ([1, 3, 5], 0),  # Odd values at odd indices are excluded.
        ([1, 2, 4, 6], 8),  # Even values at even indices are excluded.
        ([0, -2, 7, -4, 8, 6], 0),  # Negative and zero evens sum to zero.
        ([9, -8, 2, 12, 3], 4),  # Negative and positive even values are summed.
    ],
)
def test_add_sums_even_values_at_odd_indices(values, expected):
    assert add(values) == expected
