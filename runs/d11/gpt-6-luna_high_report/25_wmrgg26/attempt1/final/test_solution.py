import pytest

from solution import sum_product


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], (0, 1)),
        ([1, 2, 3, 4], (10, 24)),
        ([7], (7, 7)),
        ([0, 5, 9], (14, 0)),
        ([-2, 3, 4], (5, -24)),
        ([-2, -3], (-5, 6)),
        ([0], (0, 0)),
    ],
)
def test_sum_product(numbers, expected):
    result = sum_product(numbers)

    assert result == expected
    assert isinstance(result, tuple)
    assert len(result) == 2
