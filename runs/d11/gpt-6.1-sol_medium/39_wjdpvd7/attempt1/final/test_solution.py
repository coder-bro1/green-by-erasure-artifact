import pytest

from solution import monotonic


@pytest.mark.parametrize(
    "values, expected",
    [
        pytest.param([1, 2, 4, 20], True, id="documented-increasing"),
        pytest.param([1, 20, 4, 10], False, id="documented-mixed"),
        pytest.param([4, 1, 0, -10], True, id="documented-decreasing"),
        pytest.param([], True, id="empty"),
        pytest.param([7], True, id="single-element"),
        pytest.param([1, 2], True, id="two-increasing"),
        pytest.param([2, 1], True, id="two-decreasing"),
        pytest.param([3, 3, 3], True, id="all-equal"),
        pytest.param([1, 1, 2, 2, 3], True, id="non-strict-increasing"),
        pytest.param([3, 3, 2, 2, 1], True, id="non-strict-decreasing"),
        pytest.param([-5, -3, -1, 0], True, id="negative-increasing"),
        pytest.param([1.5, 0.0, -2.5], True, id="float-decreasing"),
        pytest.param([1, 3, 2], False, id="peak"),
        pytest.param([3, 1, 2], False, id="valley"),
        pytest.param([1, 2, 2, 1], False, id="plateau-then-reversal"),
        pytest.param([2, 1, 1, 2], False, id="valley-with-plateau"),
        pytest.param([1, 2, 1, 2], False, id="alternating"),
    ],
)
def test_monotonic(values, expected):
    assert monotonic(values) is expected


@pytest.mark.parametrize("values", [[1, 3, 2], [3, 2, 1], [1, 1, 2]])
def test_monotonic_does_not_modify_input(values):
    original = values.copy()

    monotonic(values)

    assert values == original
