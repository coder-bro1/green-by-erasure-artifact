import pytest

from solution import monotonic


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param([1, 2, 4, 20], True, id="documented-increasing"),
        pytest.param([1, 20, 4, 10], False, id="documented-nonmonotonic"),
        pytest.param([4, 1, 0, -10], True, id="documented-decreasing"),
        pytest.param([], True, id="empty"),
        pytest.param([7], True, id="single-element"),
        pytest.param([1, 2], True, id="two-increasing"),
        pytest.param([2, 1], True, id="two-decreasing"),
        pytest.param([2, 2], True, id="two-equal"),
        pytest.param([3, 3, 3, 3], True, id="constant"),
        pytest.param([1, 1, 2, 2, 3, 3], True, id="increasing-with-duplicates"),
        pytest.param([3, 3, 2, 2, 1, 1], True, id="decreasing-with-duplicates"),
        pytest.param([-10, -5, -1], True, id="negative-increasing"),
        pytest.param([-1, -5, -10], True, id="negative-decreasing"),
        pytest.param([-2, 0, 3], True, id="crossing-zero"),
        pytest.param([-1.5, -1.5, 0.0, 2.75], True, id="floats"),
        pytest.param([1, 3, 2], False, id="peak"),
        pytest.param([3, 1, 2], False, id="valley"),
        pytest.param([1, 1, 2, 2, 1], False, id="duplicates-with-reversal"),
        pytest.param([1, 2, 3, 0], False, id="reversal-at-end"),
        pytest.param([3, 1, 2, 3], False, id="reversal-at-start"),
        pytest.param([-3, -1, -2], False, id="negative-nonmonotonic"),
    ],
)
def test_monotonic(values, expected):
    assert monotonic(values) is expected


@pytest.mark.parametrize("values", [[1, 2, 3], [3, 2, 1], [2, 3, 1]])
def test_monotonic_does_not_modify_input(values):
    original = values.copy()

    monotonic(values)

    assert values == original
