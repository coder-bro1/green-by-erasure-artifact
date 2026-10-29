import pytest

from solution import add


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([4, 2, 6, 7], 2),  # The example: only index 1 qualifies.
        ([1, 2, 3, 4, 5, 6], 12),  # Even values at odd indices: 2 + 4 + 6.
        ([8, 3, 10, 5, 12], 0),  # An even value at an even index is excluded.
        ([1, -2, 3, -4, 5], -6),  # Negative even values are included.
        ([1, 3, 5, 7], 0),  # No even values.
        ([2], 0),  # A one-element list has no odd indices.
        ([0, 0], 0),  # Zero at an odd index contributes zero.
    ],
)
def test_add_sums_even_values_at_odd_indices(values, expected):
    assert add(values) == expected

