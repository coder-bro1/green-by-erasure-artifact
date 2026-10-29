import pytest

from solution import intersperse


@pytest.mark.parametrize(
    "numbers, delimiter, expected",
    [
        ([], 4, []),
        ([1], 4, [1]),
        ([1, 2], 4, [1, 4, 2]),
        ([1, 2, 3], 4, [1, 4, 2, 4, 3]),
        ([0, 0, 0], 0, [0, 0, 0, 0, 0]),
        ([-3, -2, -1], -4, [-3, -4, -2, -4, -1]),
        ([1, 2, 1], 1, [1, 1, 2, 1, 1]),
        ([5, 5, 5], 9, [5, 9, 5, 9, 5]),
    ],
)
def test_intersperse(numbers, delimiter, expected):
    assert intersperse(numbers, delimiter) == expected


@pytest.mark.parametrize("numbers", [[], [1], [1, 2, 3]])
def test_intersperse_returns_new_list_without_modifying_input(numbers):
    original = numbers.copy()

    result = intersperse(numbers, 4)

    assert numbers == original
    assert result is not numbers
    result.append(99)
    assert numbers == original
