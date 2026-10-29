import pytest

from solution import is_one_direction


@pytest.mark.parametrize(
    "seq",
    [
        [1, 1, 3],  # docstring example
        [5, 2, 2, 0],  # docstring example
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [7, 7, 7],
        [-3, -1, 0, 10],
        [1.5, 1.5, 0.2],
        ["a", "b", "c"],
    ],
)
def test_monotonic_sequences_return_true(seq):
    assert is_one_direction(seq) is True


@pytest.mark.parametrize(
    "seq",
    [
        [2, 9, 4],  # docstring example
        [1, 3, 2],
        [3, 1, 2],
        [1, 2, 2, 1],
        [5, 4, 6],
        [0, 1, 0, 1],
    ],
)
def test_non_monotonic_sequences_return_false(seq):
    assert is_one_direction(seq) is False


@pytest.mark.parametrize("seq", [[], [42]])
def test_trivial_sequences_are_one_direction(seq):
    assert is_one_direction(seq) is True


def test_does_not_mutate_input():
    seq = [3, 1, 2]
    is_one_direction(seq)
    assert seq == [3, 1, 2]
