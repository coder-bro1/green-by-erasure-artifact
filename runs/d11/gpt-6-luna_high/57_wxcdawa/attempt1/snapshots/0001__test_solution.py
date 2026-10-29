import pytest

from solution import monotonic


@pytest.mark.parametrize(
    "values",
    [
        [1, 2, 4, 20],  # strictly increasing
        [1, 2, 2, 4],  # non-decreasing with duplicates
        [4, 1, 0, -10],  # strictly decreasing
        [5, 5, 5],  # constant
        [42],  # one element
        [],  # empty sequence is monotonic
    ],
)
def test_monotonic_accepts_increasing_or_decreasing_lists(values):
    assert monotonic(values) is True


@pytest.mark.parametrize(
    "values",
    [
        [1, 20, 4, 10],
        [3, 1, 2],
        [1, 3, 2],
        [2, 1, 1, 3],
    ],
)
def test_monotonic_rejects_lists_that_change_direction(values):
    assert monotonic(values) is False


def test_monotonic_does_not_modify_the_input_list():
    values = [3, 1, 2]
    original = values.copy()

    monotonic(values)

    assert values == original
