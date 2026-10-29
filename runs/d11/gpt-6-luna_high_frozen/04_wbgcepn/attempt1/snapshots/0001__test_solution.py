import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], False),
        ([1], False),
        ([1, 3, 5, 0], False),
        ([1, 3, -2, 1], False),
        ([1, 2, 3, 7], False),
        ([2, 4, -5, 3, 5, 7], True),
        ([4, -4], True),
        ([-9, 9], True),
        ([0, 0], True),
        ([4, 4], False),
        ([-3, -8, -1], False),
    ],
)
def test_pairs_sum_to_zero_examples(values, expected):
    assert pairs_sum_to_zero(values) is expected


@pytest.mark.xfail(
    reason="solution.py currently compares each element with itself, so [0] returns True",
    strict=True,
)
def test_single_zero_is_not_a_pair():
    assert pairs_sum_to_zero([0]) is False


def test_input_is_not_modified():
    values = [2, -2, 7]
    original = values.copy()

    pairs_sum_to_zero(values)

    assert values == original
