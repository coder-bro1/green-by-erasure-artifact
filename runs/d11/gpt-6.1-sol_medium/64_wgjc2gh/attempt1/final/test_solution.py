import pytest

from solution import intersperse


@pytest.mark.parametrize(
    ("numbers", "delimiter", "expected"),
    [
        ([], 4, []),
        ([7], 4, [7]),
        ([1, 2], 9, [1, 9, 2]),
        ([1, 2, 3], 4, [1, 4, 2, 4, 3]),
        ([-3, 0, 5], -1, [-3, -1, 0, -1, 5]),
        ([1, 2, 3], 0, [1, 0, 2, 0, 3]),
        ([2, 2, 2], 2, [2, 2, 2, 2, 2]),
    ],
    ids=["empty", "singleton", "pair", "docstring", "negative", "zero", "repeated"],
)
def test_intersperse(numbers, delimiter, expected):
    assert intersperse(numbers, delimiter) == expected


@pytest.mark.parametrize("numbers", [[], [7], [1, 2, 3]])
def test_intersperse_returns_new_list_without_mutating_input(numbers):
    original = numbers.copy()

    result = intersperse(numbers, 4)

    assert numbers == original
    assert result is not numbers
    result.append(99)
    assert numbers == original


def test_intersperse_long_list_preserves_order_and_separator_positions():
    numbers = list(range(1000))

    result = intersperse(numbers, -1)

    assert len(result) == 2 * len(numbers) - 1
    assert result[::2] == numbers
    assert result[1::2] == [-1] * (len(numbers) - 1)
