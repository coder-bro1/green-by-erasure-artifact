import pytest

from solution import intersperse


@pytest.mark.parametrize(
    ("numbers", "delimiter", "expected"),
    [
        ([], 4, []),
        ([1], 4, [1]),
        ([1, 2, 3], 4, [1, 4, 2, 4, 3]),
        ([7, 7, 7], 7, [7, 7, 7, 7, 7]),
        ([1, 2], -1, [1, -1, 2]),
        ([-3, 0, 5], 0, [-3, 0, 0, 0, 5]),
    ],
)
def test_intersperse(numbers, delimiter, expected):
    assert intersperse(numbers, delimiter) == expected


def test_intersperse_does_not_modify_input():
    numbers = [1, 2, 3]
    original = numbers.copy()

    intersperse(numbers, 0)

    assert numbers == original

