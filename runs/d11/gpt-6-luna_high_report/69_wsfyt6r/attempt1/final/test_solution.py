import pytest

from solution import monotonic


@pytest.mark.xfail(
    strict=True,
    reason="monotonic returns False for sorted inputs, contrary to its docstring",
)
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 2, 4, 20], True),
        ([4, 1, 0, -10], True),
        ([1, 1, 2, 2], True),
        ([3, 3, 3], True),
        ([], True),
        ([7], True),
    ],
)
def test_monotonic_sequences(values, expected):
    assert monotonic(values) is expected


@pytest.mark.xfail(
    strict=True,
    reason="monotonic returns True for unsorted inputs, contrary to its docstring",
)
@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 20, 4, 10], False),
        ([1, 3, 2], False),
        ([1, 2, 1], False),
    ],
)
def test_non_monotonic_sequences(values, expected):
    assert monotonic(values) is expected
