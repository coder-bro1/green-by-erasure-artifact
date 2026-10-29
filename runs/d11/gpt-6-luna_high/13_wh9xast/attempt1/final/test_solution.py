import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    "numbers",
    [
        [],
        [5],
        [1, 2, 3, 4, 5],
        [1, 2, 2, 3, 3, 4],
        [0, 0, 1, 1, 2, 2],
    ],
)
def test_is_sorted_accepts_ascending_lists_with_at_most_two_of_each_value(numbers):
    assert is_sorted(numbers) is True


@pytest.mark.parametrize(
    "numbers",
    [
        [1, 3, 2, 4],
        [3, 2, 1],
        [1, 2, 2, 2, 3],
        [4, 4, 4],
    ],
)
def test_is_sorted_rejects_descending_steps_or_more_than_two_occurrences(numbers):
    assert is_sorted(numbers) is False
