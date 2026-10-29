import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([], False, id="empty"),
        pytest.param([1], False, id="single-positive"),
        pytest.param([-1], False, id="single-negative"),
        pytest.param([1, 3, -2, 1], False, id="docstring-mixed-no-pair"),
        pytest.param([1, 2, 3, 7], False, id="docstring-positive-only"),
        pytest.param([2, 4, -5, 3, 5, 7], True, id="docstring-pair"),
        pytest.param([-1, -2, -3], False, id="negative-only"),
        pytest.param([4, 4], False, id="duplicate-nonzero"),
        pytest.param([1, -1], True, id="positive-before-negative"),
        pytest.param([-1, 1], True, id="negative-before-positive"),
        pytest.param([8, 3, -8], True, id="pair-at-ends"),
        pytest.param([9, -4, 4, 2], True, id="pair-in-middle"),
        pytest.param([2, 2, -2], True, id="duplicates-with-pair"),
        pytest.param([0, 0], True, id="two-distinct-zero-positions"),
        pytest.param([10**100, -(10**100)], True, id="large-integers"),
        pytest.param([10**100, -(10**100) + 1], False, id="large-near-miss"),
    ],
)
def test_pairs_sum_to_zero(values, expected):
    original = values.copy()

    assert pairs_sum_to_zero(values) is expected
    assert values == original


@pytest.mark.xfail(
    strict=True,
    reason="The implementation pairs a zero with itself instead of requiring two positions.",
)
@pytest.mark.parametrize(
    "values",
    [
        pytest.param([0], id="single-zero"),
        pytest.param([1, 3, 5, 0], id="docstring-single-zero"),
        pytest.param([0, 2, -3], id="zero-with-unmatched-integers"),
    ],
)
def test_single_zero_does_not_form_a_pair(values):
    assert pairs_sum_to_zero(values) is False
