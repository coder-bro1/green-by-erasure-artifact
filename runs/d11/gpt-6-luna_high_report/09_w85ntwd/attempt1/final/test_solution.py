import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 3, 5, 0], False),
        ([1, 3, -2, 1], False),
        ([1, 2, 3, 7], False),
        ([2, 4, -5, 3, 5, 7], True),
        ([1], False),
        ([], False),
        ([-8, 8], True),
        ([0], False),
        ([0, 0], True),
        ([4, 4, -4], True),
        ([-3, -2, -1], False),
        ([10**100, -(10**100)], True),
    ],
)
def test_pairs_sum_to_zero(values, expected):
    assert pairs_sum_to_zero(values) is expected


def test_does_not_mutate_input_list():
    values = [4, -1, 2]
    original = values.copy()

    pairs_sum_to_zero(values)

    assert values == original
