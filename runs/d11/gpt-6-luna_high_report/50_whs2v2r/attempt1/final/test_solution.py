import pytest

from solution import monotonic


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 2, 4, 20], True),
        ([1, 20, 4, 10], False),
        ([4, 1, 0, -10], True),
        ([-10, 0, 1, 4], True),
        ([1, 1, 2, 2], True),
        ([5, 3, 3, 1], True),
        ([7, 7, 7], True),
        ([], True),
        ([42], True),
        ([1, 3, 2], False),
        ([3, 1, 2], False),
        ([1, 2, 1], False),
    ],
)
def test_monotonic(values, expected):
    assert monotonic(values) is expected
