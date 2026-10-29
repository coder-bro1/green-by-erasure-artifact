import pytest

from solution import monotonic


@pytest.mark.parametrize(
    "seq",
    [
        [1, 2, 4, 20],        # docstring example
        [4, 1, 0, -10],       # docstring example
        [1, 2, 2, 3],         # non-strict increasing
        [3, 3, 2, 1],         # non-strict decreasing
        [5, 5, 5],            # constant
        [7],                  # single element
        [],                   # empty
        [1.5, 2.5, 10.0],     # floats
    ],
)
def test_monotonic_true(seq):
    assert monotonic(seq) is True


@pytest.mark.parametrize(
    "seq",
    [
        [1, 20, 4, 10],       # docstring example
        [1, 3, 2],
        [3, 1, 2],
        [1, 2, 3, 2, 1],
    ],
)
def test_monotonic_false(seq):
    assert monotonic(seq) is False


def test_does_not_mutate_input():
    seq = [3, 1, 2]
    monotonic(seq)
    assert seq == [3, 1, 2]
