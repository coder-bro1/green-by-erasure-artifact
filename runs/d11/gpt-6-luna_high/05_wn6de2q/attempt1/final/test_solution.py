import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (3, 5, 1),
        (25, 15, 5),
        (54, 24, 6),
        (17, 17, 17),
        (0, 9, 9),
        (9, 0, 9),
        (0, 0, 0),
        (-25, 15, 5),
        (25, -15, 5),
        (-25, -15, 5),
        (-7, 0, 7),
    ],
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected


def test_greatest_common_divisor_is_symmetric():
    assert greatest_common_divisor(84, 30) == greatest_common_divisor(30, 84)
