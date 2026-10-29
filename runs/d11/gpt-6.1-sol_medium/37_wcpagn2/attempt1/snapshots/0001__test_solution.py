import pytest

from solution import count_nums


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([-1, 11, -11], 1, id="documented-signed-digits"),
        pytest.param([1, 1, 2], 3, id="documented-duplicates"),
        pytest.param([0, 0, 0], 0, id="zeros"),
        pytest.param(list(range(1, 10)), 9, id="positive-single-digits"),
        pytest.param(list(range(-9, 0)), 0, id="negative-single-digits"),
        pytest.param([10, 100, 1000, 9000], 4, id="positive-trailing-zeros"),
        pytest.param([-10, -100, -1000, -9000], 0, id="negative-trailing-zeros"),
        pytest.param([-11, -22, -101, -202, -9009], 0, id="signed-sum-zero"),
        pytest.param([-12, -123, -109, -9099], 4, id="negative-with-positive-sum"),
        pytest.param([-21, -310, -8007, -9001], 0, id="negative-with-negative-sum"),
        pytest.param([-21, -22, -23], 1, id="strict-positive-boundary"),
        pytest.param([-12, -12, -11, 0, 5, 5], 4, id="count-occurrences"),
        pytest.param([0, -1, 1, -11, -12, -21, 100, -123], 4, id="mixed-signs"),
        pytest.param(
            [10**100, -(10**100), -(10**100 + 1), -(10**100 + 2)],
            2,
            id="arbitrary-precision-integers",
        ),
    ],
)
def test_count_nums(numbers, expected):
    assert count_nums(numbers) == expected


def test_count_nums_does_not_modify_input():
    numbers = [-123, 0, 11, -11, 11]
    original = numbers.copy()

    assert count_nums(numbers) == 3
    assert numbers == original


def test_count_nums_is_independent_of_order():
    numbers = [-123, -22, 0, 9, -10, 101, -23]

    assert count_nums(numbers) == count_nums(numbers[::-1]) == 4
