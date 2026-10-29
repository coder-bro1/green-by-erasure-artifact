import pytest

from solution import rolling_max


def test_empty_list():
    assert rolling_max([]) == []


def test_single_element():
    assert rolling_max([7]) == [7]


def test_docstring_example():
    assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]


def test_strictly_increasing():
    assert rolling_max([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_strictly_decreasing():
    assert rolling_max([4, 3, 2, 1]) == [4, 4, 4, 4]


def test_all_equal():
    assert rolling_max([3, 3, 3]) == [3, 3, 3]


def test_negative_numbers():
    assert rolling_max([-5, -3, -4, -1, -2]) == [-5, -3, -3, -1, -1]


def test_max_at_end():
    assert rolling_max([3, 2, 1, 5]) == [3, 3, 3, 5]


def test_does_not_mutate_input():
    data = [1, 3, 2]
    rolling_max(data)
    assert data == [1, 3, 2]


def test_output_length_matches_input():
    data = [5, 1, 9, 2, 8]
    assert len(rolling_max(data)) == len(data)


@pytest.mark.parametrize(
    "data",
    [[2, 1, 4, 3], [0, -1, 10, 5, 11], [9], [1, 1, 2, 2, 1]],
)
def test_matches_reference_implementation(data):
    expected, cur = [], None
    for n in data:
        cur = n if cur is None else max(cur, n)
        expected.append(cur)
    assert rolling_max(data) == expected
