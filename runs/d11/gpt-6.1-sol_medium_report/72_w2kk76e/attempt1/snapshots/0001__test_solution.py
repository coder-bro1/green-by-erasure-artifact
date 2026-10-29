import pytest

from solution import sum_product


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], (0, 1), id="empty-list"),
        pytest.param([1, 2, 3, 4], (10, 24), id="docstring-example"),
        pytest.param([7], (7, 7), id="single-positive"),
        pytest.param([-7], (-7, -7), id="single-negative"),
        pytest.param([1, 1, 1], (3, 1), id="multiplicative-identity"),
        pytest.param([-2, 3, 4], (5, -24), id="odd-negative-count"),
        pytest.param([-2, -3, 4], (-1, 24), id="even-negative-count"),
        pytest.param([-3, 3], (0, -9), id="zero-sum-nonzero-product"),
        pytest.param([2, 2, 2], (6, 8), id="repeated-values"),
        pytest.param([10**30, 10**30], (2 * 10**30, 10**60), id="large-integers"),
        pytest.param([0], (0, 0), id="single-zero"),
        pytest.param([0, 2, -3], (-1, 0), id="leading-zero"),
        pytest.param([2, 0, -3], (-1, 0), id="middle-zero"),
        pytest.param([2, -3, 0], (-1, 0), id="trailing-zero"),
        pytest.param([0, 0, 0], (0, 0), id="all-zeros"),
    ],
)
def test_sum_product(numbers, expected):
    result = sum_product(numbers)

    assert isinstance(result, tuple)
    assert result == expected
