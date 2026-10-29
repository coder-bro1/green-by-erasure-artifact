import pytest

from solution import monotonic


@pytest.mark.parametrize(
    "values",
    [
        [1, 2, 4, 20],
        [4, 1, 0, -10],
        [],
        [7],
        [3, 3, 3],
        [1, 2, 2, 4],
        [4, 2, 2, 1],
    ],
)
def test_monotonic_sequences_return_true(values):
    assert monotonic(values) is True


@pytest.mark.parametrize(
    "values",
    [
        [1, 20, 4, 10],
        [1, 3, 2],
        [3, 1, 2],
    ],
)
def test_non_monotonic_sequences_return_false(values):
    assert monotonic(values) is False
