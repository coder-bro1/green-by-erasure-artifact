"""Regression tests for the current behavior of solution.monotonic.

The implementation returns the opposite of the result described by its
docstring. These tests intentionally preserve that behavior because
solution.py must remain unchanged.
"""

import pytest

from solution import monotonic


@pytest.mark.parametrize(
    "values",
    [
        pytest.param([], id="empty"),
        pytest.param([7], id="singleton"),
        pytest.param([1, 2], id="ascending-pair"),
        pytest.param([2, 1], id="descending-pair"),
        pytest.param([1, 2, 4, 20], id="ascending-docstring-example"),
        pytest.param([4, 1, 0, -10], id="descending-docstring-example"),
        pytest.param([3, 3, 3], id="constant"),
        pytest.param([1, 1, 2, 2, 3], id="nondecreasing"),
        pytest.param([3, 3, 2, 2, 1], id="nonincreasing"),
        pytest.param([-10, -4, -1, 0], id="negative-values"),
        pytest.param([-1.5, 0.0, 2.5], id="floats"),
    ],
)
def test_ordered_lists_return_false(values):
    assert monotonic(values) is False


@pytest.mark.parametrize(
    "values",
    [
        pytest.param([1, 20, 4, 10], id="unordered-docstring-example"),
        pytest.param([1, 3, 2], id="peak"),
        pytest.param([3, 1, 2], id="valley"),
        pytest.param([1, 2, 1, 2], id="alternating"),
        pytest.param([1, 1, 2, 1], id="duplicates-with-reversal"),
        pytest.param([-3, -1, -2], id="negative-reversal"),
        pytest.param([0.5, -0.5, 1.5], id="float-reversal"),
    ],
)
def test_unordered_lists_return_true(values):
    assert monotonic(values) is True


@pytest.mark.parametrize("values", [[1, 2, 3], [3, 2, 1], [3, 1, 2]])
def test_input_list_is_not_modified(values):
    original = values.copy()

    monotonic(values)

    assert values == original
