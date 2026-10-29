import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1, 3, 5, 0], False, id="docstring-single-zero"),
        pytest.param([1, 3, -2, 1], False, id="docstring-unmatched-negative"),
        pytest.param([1, 2, 3, 7], False, id="docstring-positive-only"),
        pytest.param([2, 4, -5, 3, 5, 7], True, id="docstring-matching-pair"),
        pytest.param([1], False, id="docstring-single-positive"),
        pytest.param([], False, id="empty"),
        pytest.param([0], False, id="single-zero-cannot-pair-with-itself"),
        pytest.param([-1], False, id="single-negative"),
        pytest.param([0, 0], True, id="two-distinct-zeros"),
        pytest.param([0, 0, 0], True, id="multiple-zeros"),
        pytest.param([5, -5], True, id="positive-then-negative"),
        pytest.param([-5, 5], True, id="negative-then-positive"),
        pytest.param([-1, -2, -3], False, id="negative-only"),
        pytest.param([2, 2], False, id="duplicate-nonzero"),
        pytest.param([-2, -2, 2], True, id="duplicates-with-opposite"),
        pytest.param([0, 2, -2], True, id="zero-and-nonzero-pair"),
        pytest.param([-8, 1, 3, 8], True, id="pair-at-ends"),
        pytest.param([9, 3, -3, 7], True, id="pair-in-middle"),
        pytest.param([1, 2, -3], False, id="only-three-element-sum-is-zero"),
        pytest.param([10**100, -(10**100)], True, id="large-integers"),
        pytest.param([10**100, -(10**100) + 1], False, id="large-near-match"),
    ],
)
def test_pairs_sum_to_zero(values, expected):
    original = values.copy()

    assert pairs_sum_to_zero(values) is expected
    assert values == original


@pytest.mark.parametrize("values", [[1, 3, -3, 8], [0], [0, 0], [1, 2, -3]])
def test_result_does_not_depend_on_order(values):
    assert pairs_sum_to_zero(values) is pairs_sum_to_zero(list(reversed(values)))
