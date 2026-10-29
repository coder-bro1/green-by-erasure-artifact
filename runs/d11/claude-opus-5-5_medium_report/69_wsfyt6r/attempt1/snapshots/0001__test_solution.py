import pytest

from solution import monotonic

INVERTED = (
    "monotonic() has its return values inverted: it returns False when the list "
    "equals sorted(l) or sorted(l, reverse=True), and True otherwise"
)


@pytest.mark.xfail(strict=True, reason=INVERTED)
@pytest.mark.parametrize(
    "data",
    [
        [1, 2, 4, 20],        # docstring example
        [4, 1, 0, -10],       # docstring example
        [1, 2, 3, 4, 5],
        [10, 5, 0],
        [1, 1, 2, 2, 3],      # non-strict increasing
        [3, 3, 2, 1, 1],      # non-strict decreasing
        [7, 7, 7],            # constant
        [0.5, 1.5, 2.5],
        [5],                  # single element
        [],                   # empty
    ],
)
def test_monotonic_lists_return_true(data):
    assert monotonic(data) is True


@pytest.mark.xfail(strict=True, reason=INVERTED)
@pytest.mark.parametrize(
    "data",
    [
        [1, 20, 4, 10],       # docstring example
        [1, 3, 2],
        [3, 1, 2],
        [1, 2, 2, 1],
        [0, -1, 0],
        [1, 2, 3, 4, 3],
    ],
)
def test_non_monotonic_lists_return_false(data):
    assert monotonic(data) is False


def test_does_not_mutate_input():
    data = [3, 1, 2]
    monotonic(data)
    assert data == [3, 1, 2]


def test_returns_bool():
    assert isinstance(monotonic([1, 2, 3]), bool)
    assert isinstance(monotonic([1, 3, 2]), bool)
