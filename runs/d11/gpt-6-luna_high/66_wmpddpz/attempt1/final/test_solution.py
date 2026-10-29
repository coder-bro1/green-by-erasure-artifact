from solution import intersperse


def test_intersperse_empty_list():
    assert intersperse([], 4) == []


def test_intersperse_single_element():
    assert intersperse([7], 4) == [7]


def test_intersperse_between_each_pair():
    assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]


def test_intersperse_handles_negative_values_and_delimiter():
    assert intersperse([-2, 0, 5], -1) == [-2, -1, 0, -1, 5]


def test_intersperse_does_not_modify_input():
    numbers = [1, 2, 3]

    intersperse(numbers, 4)

    assert numbers == [1, 2, 3]
