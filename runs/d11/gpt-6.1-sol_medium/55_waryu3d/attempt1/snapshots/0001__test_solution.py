import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([1, 3, 2, 0], 10, id="documented-mixed-example"),
        pytest.param([-1, -2, 0], 0, id="documented-negative-example"),
        pytest.param([9, -2], 81, id="documented-single-positive-example"),
        pytest.param([0], 0, id="zero"),
        pytest.param([1], 1, id="smallest-positive-odd"),
        pytest.param([7], 49, id="single-odd"),
        pytest.param([2, 4, 6, 100], 0, id="positive-evens"),
        pytest.param([-9, -7, -3, -1], 0, id="negative-odds"),
        pytest.param([1, 3, 5, 7, 9], 165, id="positive-odds"),
        pytest.param([3, 3, 3], 27, id="duplicates-count-individually"),
        pytest.param([0, 0, 5, 0], 25, id="zeros-among-odds"),
        pytest.param([0.5, 1.5, 2.5, 3.5], 0, id="fractional-floats"),
        pytest.param([1.0, 3.0, 5.0], 0, id="integer-valued-floats"),
        pytest.param([-1.5, -3.0, 0.0, 2.0], 0, id="other-floats"),
        pytest.param(
            [-5, 4, 3.0, 7, 1.5, 1, 0, -2.5],
            50,
            id="mixed-integers-and-floats",
        ),
        pytest.param([10**30 + 1], (10**30 + 1) ** 2, id="large-odd-integer"),
        pytest.param([10**30, -(10**30 + 1)], 0, id="large-excluded-integers"),
    ],
)
def test_double_the_difference(numbers, expected):
    result = double_the_difference(numbers)

    assert result == expected
    assert type(result) is int


def test_input_is_not_modified():
    numbers = [5, -3, 1.5, 2, 1, 5]
    original = numbers.copy()

    assert double_the_difference(numbers) == 51
    assert numbers == original


def test_consecutive_positive_and_negative_numbers():
    # There are 50 positive odd integers through 100. Their squared sum
    # follows n * (4 * n**2 - 1) / 3.
    numbers = list(range(-100, 101))
    expected = 50 * (4 * 50**2 - 1) // 3

    assert double_the_difference(numbers) == expected


def test_order_does_not_change_the_result():
    numbers = [9, -5, 2.5, 3, 0, 4, 1]

    assert double_the_difference(numbers) == 91
    assert double_the_difference(list(reversed(numbers))) == 91
