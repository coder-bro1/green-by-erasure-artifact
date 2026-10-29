import pytest

from solution import rolling_max


def test_docstring_example():
    assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]


def test_empty_list():
    assert rolling_max([]) == []


def test_single_element():
    assert rolling_max([7]) == [7]


def test_strictly_increasing():
    assert rolling_max([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_strictly_decreasing():
    assert rolling_max([4, 3, 2, 1]) == [4, 4, 4, 4]


def test_all_equal():
    assert rolling_max([5, 5, 5]) == [5, 5, 5]


def test_negative_numbers():
    assert rolling_max([-3, -5, -1, -2]) == [-3, -3, -1, -1]


def test_zero_handled_as_first_element():
    # 0 is falsy; make sure it is not treated like "no max yet".
    assert rolling_max([0, -1, -2]) == [0, 0, 0]


def test_mixed_signs():
    assert rolling_max([-2, 0, -1, 3, 1]) == [-2, 0, 0, 3, 3]


def test_does_not_mutate_input():
    data = [3, 1, 2]
    rolling_max(data)
    assert data == [3, 1, 2]


def test_returns_new_list_same_length():
    data = [1, 2, 3]
    result = rolling_max(data)
    assert result is not data
    assert len(result) == len(data)


@pytest.mark.parametrize(
    "numbers",
    [[3, 1, 4, 1, 5, 9, 2, 6], [10, -10, 20, -20], list(range(50, 0, -1))],
)
def test_matches_reference(numbers):
    expected = [max(numbers[: i + 1]) for i in range(len(numbers))]
    assert rolling_max(numbers) == expected
