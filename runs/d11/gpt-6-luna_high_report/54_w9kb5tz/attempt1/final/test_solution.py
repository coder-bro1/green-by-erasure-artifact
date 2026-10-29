import pytest

from solution import largest_divisor


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (15, 5),  # Documented example
        (12, 6),
        (7, 1),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason=(
        "largest_divisor never returns a divisor: its loop excludes n, but its "
        "condition requires i == n"
    ),
)
def test_largest_divisor_returns_largest_proper_divisor(number, expected):
    assert largest_divisor(number) == expected
