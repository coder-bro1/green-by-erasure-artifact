import pytest

from solution import sum_product


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], (0, 1), id="empty-list"),
        pytest.param([1, 2, 3, 4], (10, 24), id="docstring-example"),
        pytest.param([7], (7, 7), id="positive-singleton"),
        pytest.param([-7], (-7, -7), id="negative-singleton"),
        pytest.param([0], (0, 0), id="zero-singleton"),
        pytest.param([2, 0, -3], (-1, 0), id="zero-in-list"),
        pytest.param([-2, -3, -4], (-9, -24), id="odd-negative-count"),
        pytest.param([-2, -3, 4], (-1, 24), id="even-negative-count"),
        pytest.param([-5, 5], (0, -25), id="cancelling-sum"),
        pytest.param([3, 3, 3], (9, 27), id="repeated-values"),
        pytest.param([1, 1, 1], (3, 1), id="multiplicative-identity"),
        pytest.param(
            [10**100, 10**100],
            (2 * 10**100, 10**200),
            id="arbitrary-precision-integers",
        ),
    ],
)
def test_sum_product_documented_behavior(numbers, expected):
    result = sum_product(numbers)

    assert isinstance(result, tuple)
    assert result == expected


def test_sum_product_does_not_modify_input():
    numbers = [4, -2, 3, 4]
    original = numbers.copy()

    assert sum_product(numbers) == (9, -96)
    assert numbers == original


def test_sum_product_is_independent_of_order():
    numbers = [2, -3, 5, -7]

    assert sum_product(numbers) == ( -3, 210)
    assert sum_product(list(reversed(numbers))) == (-3, 210)
