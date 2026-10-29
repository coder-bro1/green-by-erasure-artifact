import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], False),
        ([1], False),
        ([0], False),
        ([1, 3, 5, 0], False),
        ([1, 3, -2, 1], False),
        ([1, 2, 3, 7], False),
        ([2, 4, -5, 3, 5, 7], True),
        ([0, 0], True),
        ([4, -4], True),
        ([-6, 2, 6], True),
    ],
)
def test_pairs_sum_to_zero(values, expected):
    assert pairs_sum_to_zero(values) is expected
