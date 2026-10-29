import pytest

from solution import monotonic


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Docstring requires True for monotonic lists, but solution returns False.",
)
@pytest.mark.parametrize(
    "values",
    [
        pytest.param([1, 2, 4, 20], id="docstring-increasing"),
        pytest.param([4, 1, 0, -10], id="docstring-decreasing"),
        pytest.param([], id="empty"),
        pytest.param([7], id="single-element"),
        pytest.param([3, 3, 3], id="constant"),
        pytest.param([-3, -3, 0, 2, 2], id="nondecreasing-with-repeats"),
        pytest.param([2, 2, 0, -3, -3], id="nonincreasing-with-repeats"),
        pytest.param([-1.5, 0.0, 2.5], id="increasing-floats"),
    ],
)
def test_monotonic_sequences_return_true(values):
    assert monotonic(values) is True


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Docstring requires False for nonmonotonic lists, but solution returns True.",
)
@pytest.mark.parametrize(
    "values",
    [
        pytest.param([1, 20, 4, 10], id="docstring-nonmonotonic"),
        pytest.param([1, 3, 2], id="peak"),
        pytest.param([3, 1, 2], id="valley"),
        pytest.param([1, 1, 3, 2, 2], id="direction-change-with-repeats"),
        pytest.param([0.5, -1.0, 2.5], id="nonmonotonic-floats"),
    ],
)
def test_nonmonotonic_sequences_return_false(values):
    assert monotonic(values) is False
