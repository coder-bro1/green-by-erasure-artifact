import pytest

from solution import monotonic


@pytest.mark.parametrize(
    "seq, expected",
    [
        # Docstring examples
        ([1, 2, 4, 20], True),
        ([1, 20, 4, 10], False),
        ([4, 1, 0, -10], True),
        # Edge cases
        ([], True),
        ([5], True),
        ([3, 3], True),
        ([7, 7, 7, 7], True),
        # Non-strict monotonic (repeated values allowed)
        ([1, 2, 2, 3], True),
        ([3, 2, 2, 1], True),
        ([1, 1, 2, 2, 3, 3], True),
        # Non-monotonic
        ([1, 2, 1], False),
        ([2, 1, 2], False),
        ([1, 2, 3, 2], False),
        ([3, 2, 1, 2], False),
        ([1, 1, 0, 1], False),
        # Floats and negatives
        ([-5.5, -1.0, 0.0, 2.25], True),
        ([0.3, 0.2, 0.1], True),
        ([0.1, 0.3, 0.2], False),
        # Large range
        (list(range(1000)), True),
        (list(range(1000, 0, -1)), True),
    ],
)
def test_monotonic(seq, expected):
    assert monotonic(seq) is expected


def test_returns_bool():
    assert isinstance(monotonic([1, 2]), bool)
    assert isinstance(monotonic([2, 1, 2]), bool)


def test_does_not_mutate_input():
    data = [3, 1, 2]
    monotonic(data)
    assert data == [3, 1, 2]


def test_works_with_strings():
    assert monotonic(["a", "b", "c"]) is True
    assert monotonic(["c", "b", "a"]) is True
    assert monotonic(["a", "c", "b"]) is False
