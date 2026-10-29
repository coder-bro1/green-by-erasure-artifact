from solution import rolling_max


def test_rolling_max_example():
    assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]


def test_rolling_max_empty_input():
    assert rolling_max([]) == []


def test_rolling_max_single_value():
    assert rolling_max([7]) == [7]


def test_rolling_max_decreasing_values():
    assert rolling_max([5, 4, 3, 2]) == [5, 5, 5, 5]


def test_rolling_max_negative_values():
    assert rolling_max([-8, -3, -5, -1, -7]) == [-8, -3, -3, -1, -1]


def test_rolling_max_repeated_maximum():
    assert rolling_max([2, 6, 6, 1, 6]) == [2, 6, 6, 6, 6]


def test_rolling_max_does_not_modify_input():
    numbers = [3, 1, 4, 2]
    original = numbers.copy()

    rolling_max(numbers)

    assert numbers == original
