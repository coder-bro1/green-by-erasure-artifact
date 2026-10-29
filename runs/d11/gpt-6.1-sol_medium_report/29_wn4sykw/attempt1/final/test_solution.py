import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    "values, expected",
    [
        pytest.param([1, 3, -2, 1], False, id="docstring-mixed-no-pair"),
        pytest.param([1, 2, 3, 7], False, id="docstring-positive-only"),
        pytest.param([2, 4, -5, 3, 5, 7], True, id="docstring-pair"),
        pytest.param([1], False, id="docstring-singleton"),
    ],
)
def test_docstring_examples(values, expected):
    assert pairs_sum_to_zero(values) is expected


@pytest.mark.parametrize(
    "values, expected",
    [
        pytest.param([], False, id="empty"),
        pytest.param([-1], False, id="negative-singleton"),
        pytest.param([1, 1], False, id="positive-duplicates"),
        pytest.param([-1, -1], False, id="negative-duplicates"),
        pytest.param([-1, -2, -3], False, id="negative-only"),
        pytest.param([2, -3, 4, -5], False, id="mixed-no-pair"),
        pytest.param([1, -1], True, id="positive-then-negative"),
        pytest.param([-1, 1], True, id="negative-then-positive"),
        pytest.param([0, 0], True, id="two-zero-elements"),
        pytest.param([0, 0, 0], True, id="multiple-zero-elements"),
        pytest.param([3, 8, -3], True, id="nonadjacent-pair"),
        pytest.param([8, 3, -3], True, id="pair-at-end"),
        pytest.param([2, 2, -2], True, id="duplicates-with-opposite"),
        pytest.param([0, 7, -7], True, id="zero-and-valid-pair"),
        pytest.param([10**100, -(10**100)], True, id="large-integer-pair"),
        pytest.param([10**100, -(10**100) + 1], False, id="large-integers-no-pair"),
    ],
)
def test_pair_detection(values, expected):
    assert pairs_sum_to_zero(values) is expected


@pytest.mark.xfail(
    strict=True,
    reason="The loop allows i == j, so a single zero is paired with itself, "
    "violating the docstring's requirement for two distinct elements.",
)
@pytest.mark.parametrize(
    "values",
    [
        pytest.param([1, 3, 5, 0], id="docstring-single-zero"),
        pytest.param([0], id="zero-singleton"),
        pytest.param([0, 1], id="zero-first-no-pair"),
        pytest.param([-2, 0, 3], id="zero-middle-no-pair"),
    ],
)
def test_single_zero_without_distinct_pair_returns_false(values):
    assert pairs_sum_to_zero(values) is False


@pytest.mark.parametrize("values", [[], [1, 2, 3], [2, -2, 4], [0, 0]])
def test_input_is_not_modified(values):
    original = values.copy()
    pairs_sum_to_zero(values)
    assert values == original
