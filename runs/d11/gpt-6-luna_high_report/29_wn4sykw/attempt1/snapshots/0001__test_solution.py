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
        ([1, -1], True),
        ([4, 4, -4], True),
        ([0, 0], True),
    ],
)
def test_pairs_sum_to_zero_examples_and_boundaries(values, expected):
    assert pairs_sum_to_zero(values) is expected


@pytest.mark.xfail(
    strict=True,
    reason="The implementation pairs an element with itself, so [0] returns True despite the docstring requiring distinct elements.",
)
def test_a_single_zero_is_not_a_pair():
    assert pairs_sum_to_zero([0]) is False
