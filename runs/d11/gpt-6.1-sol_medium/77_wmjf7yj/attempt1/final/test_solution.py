import pytest

from solution import sum_product


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], (0, 1), id="empty"),
        pytest.param([1, 2, 3, 4], (10, 24), id="documented-example"),
        pytest.param([7], (7, 7), id="single-positive"),
        pytest.param([-7], (-7, -7), id="single-negative"),
        pytest.param([0], (0, 0), id="single-zero"),
        pytest.param([2, 0, -3], (-1, 0), id="zero-in-list"),
        pytest.param([-2, 3, 4], (5, -24), id="mixed-signs"),
        pytest.param([-2, -3, -4], (-9, -24), id="odd-negative-count"),
        pytest.param([-2, -3], (-5, 6), id="even-negative-count"),
        pytest.param([5, 5, 5], (15, 125), id="repeated-values"),
        pytest.param([10**20, 10**20], (2 * 10**20, 10**40), id="large-integers"),
    ],
)
def test_sum_product(numbers, expected):
    result = sum_product(numbers)

    assert isinstance(result, tuple)
    assert result == expected


def test_sum_product_does_not_modify_input():
    numbers = [3, -2, 0, 5]
    original = numbers.copy()

    sum_product(numbers)

    assert numbers == original
