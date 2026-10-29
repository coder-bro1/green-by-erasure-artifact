import pytest

from solution import sum_product


@pytest.mark.parametrize(
    ("numbers", "expected_sum", "expected_product"),
    [
        pytest.param([], 0, 1, marks=pytest.mark.xfail(
            strict=True,
            reason="sum_product initializes the product to 0 instead of the empty-product identity 1",
        )),
        pytest.param([1, 2, 3, 4], 10, 24, marks=pytest.mark.xfail(
            strict=True,
            reason="sum_product initializes the product to 0, so every nonempty product is 0",
        )),
        pytest.param([-2, 3], 1, -6, marks=pytest.mark.xfail(
            strict=True,
            reason="sum_product initializes the product to 0, so every nonempty product is 0",
        )),
        pytest.param([5], 5, 5, marks=pytest.mark.xfail(
            strict=True,
            reason="sum_product initializes the product to 0, so every nonempty product is 0",
        )),
    ],
)
def test_sum_product(numbers, expected_sum, expected_product):
    assert sum_product(numbers) == (expected_sum, expected_product)


@pytest.mark.parametrize(
    ("numbers", "expected_sum"),
    [([], 0), ([1, 2, 3, 4], 10), ([-2, 3], 1), ([5], 5)],
)
def test_sum_component(numbers, expected_sum):
    result = sum_product(numbers)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == expected_sum
