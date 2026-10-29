import pytest

from solution import intersperse


@pytest.mark.parametrize(
    ("numbers", "delimiter", "expected"),
    [
        ([], 4, []),
        ([1, 2, 3], 4, [1, 4, 2, 4, 3]),
        ([7], 4, [7]),
        ([1, 2], 0, [1, 0, 2]),
        ([-2, 0, 5], -1, [-2, -1, 0, -1, 5]),
    ],
)
def test_intersperse(numbers, delimiter, expected):
    assert intersperse(numbers, delimiter) == expected
