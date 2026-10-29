import pytest

from solution import pairs_sum_to_zero


@pytest.mark.parametrize(
    "values, expected",
    [
        pytest.param([1, 3, 5, 0], False, id="docstring-single-zero"),
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
        pytest.param([0], False, id="zero-singleton"),
        pytest.param([0, 1], False, id="zero-first-no-pair"),
        pytest.param([-2, 0, 3], False, id="zero-middle-no-pair"),
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


@pytest.mark.parametrize("values", [[], [1, 2, 3], [2, -2, 4], [0, 0]])
def test_input_is_not_modified(values):
    original = values.copy()
    pairs_sum_to_zero(values)
    assert values == original
