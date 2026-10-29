import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (3, 5, 1),
        (25, 15, 5),
        (54, 24, 6),
        (7, 7, 7),
        (0, 9, 9),
        (9, 0, 9),
        (0, 0, 0),
        (-18, 12, 6),
        (18, -12, 6),
        (-18, -12, 6),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected
