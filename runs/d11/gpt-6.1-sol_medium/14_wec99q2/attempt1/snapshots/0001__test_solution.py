import pytest

from solution import sum_product


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], (0, 1), id="empty-list"),
        pytest.param([1, 2, 3, 4], (10, 24), id="positive-integers"),
        pytest.param([7], (7, 7), id="single-positive"),
        pytest.param([-7], (-7, -7), id="single-negative"),
        pytest.param([0], (0, 0), id="single-zero"),
        pytest.param([2, 0, -3], (-1, 0), id="zero-among-integers"),
        pytest.param([-2, -3, -4], (-9, -24), id="odd-negative-count"),
        pytest.param([-2, -3, 4], (-1, 24), id="even-negative-count"),
        pytest.param([-5, 5], (0, -25), id="canceling-sum"),
        pytest.param([3, 3, 3], (9, 27), id="repeated-values"),
        pytest.param(
            [10**100, 10**100],
            (2 * 10**100, 10**200),
            id="arbitrary-precision-integers",
        ),
    ],
)
def test_sum_product(numbers, expected):
    result = sum_product(numbers)

    assert isinstance(result, tuple)
    assert result == expected


def test_sum_product_does_not_modify_input():
    numbers = [4, -2, 0, 7]
    original = numbers.copy()

    sum_product(numbers)

    assert numbers == original


def test_sum_product_calls_are_independent():
    assert sum_product([2, 3]) == (5, 6)
    assert sum_product([]) == (0, 1)
    assert sum_product([4, 5]) == (9, 20)
