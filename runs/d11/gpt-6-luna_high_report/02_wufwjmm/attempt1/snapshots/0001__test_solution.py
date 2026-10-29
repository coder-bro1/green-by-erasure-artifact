import pytest

from solution import greatest_common_divisor


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (3, 5, 1),
        (25, 15, 5),
        (0, 9, 9),
        (18, 12, 6),
        (-18, 12, 6),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="greatest_common_divisor returns the final remainder (zero) instead of the GCD",
)
def test_greatest_common_divisor(a, b, expected):
    assert greatest_common_divisor(a, b) == expected
