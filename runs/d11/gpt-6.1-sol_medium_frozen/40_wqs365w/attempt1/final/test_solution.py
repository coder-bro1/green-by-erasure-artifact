import pytest

from solution import sum_product


PRODUCT_BUG = pytest.mark.xfail(
    strict=True,
    reason="solution.py initializes the product to 0 instead of 1",
)


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], (0, 1), marks=PRODUCT_BUG, id="empty"),
        pytest.param([7], (7, 7), marks=PRODUCT_BUG, id="single-positive"),
        pytest.param([-7], (-7, -7), marks=PRODUCT_BUG, id="single-negative"),
        pytest.param([1, 2, 3, 4], (10, 24), marks=PRODUCT_BUG, id="docstring-example"),
        pytest.param([1, 1, 1], (3, 1), marks=PRODUCT_BUG, id="ones"),
        pytest.param([-2, 3, 4], (5, -24), marks=PRODUCT_BUG, id="mixed-signs"),
        pytest.param([-2, -3, -4], (-9, -24), marks=PRODUCT_BUG, id="odd-negatives"),
        pytest.param([-2, -3], (-5, 6), marks=PRODUCT_BUG, id="even-negatives"),
        pytest.param([-5, 5], (0, -25), marks=PRODUCT_BUG, id="zero-sum"),
        pytest.param(
            [10**20, 10**20],
            (2 * 10**20, 10**40),
            marks=PRODUCT_BUG,
            id="large-integers",
        ),
        pytest.param([0], (0, 0), id="single-zero"),
        pytest.param([0, 0, 0], (0, 0), id="all-zeros"),
        pytest.param([0, 2, -3], (-1, 0), id="leading-zero"),
        pytest.param([2, 0, -3], (-1, 0), id="middle-zero"),
        pytest.param([2, -3, 0], (-1, 0), id="trailing-zero"),
    ],
)
def test_sum_product(numbers, expected):
    assert sum_product(numbers) == expected


@pytest.mark.parametrize("numbers", [[], [2, -3, 4], [0, 2, -3]])
def test_sum_product_does_not_modify_input(numbers):
    original = numbers.copy()

    sum_product(numbers)

    assert numbers == original


@pytest.mark.parametrize("numbers", [[], [2, -3, 4], [0, 2, -3]])
def test_sum_product_returns_pair_of_integers(numbers):
    result = sum_product(numbers)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(type(value) is int for value in result)
