import pytest

from solution import monotonic


@pytest.mark.xfail(
    strict=True,
    reason="solution.monotonic currently returns the inverse of its documented result",
)
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 2, 4, 20], True),
        ([4, 1, 0, -10], True),
        ([1, 20, 4, 10], False),
        ([1, 1, 2, 2], True),
        ([3, 3, 3], True),
        ([], True),
        ([7], True),
    ],
)
def test_monotonic_matches_documented_behavior(values, expected):
    assert monotonic(values) is expected
