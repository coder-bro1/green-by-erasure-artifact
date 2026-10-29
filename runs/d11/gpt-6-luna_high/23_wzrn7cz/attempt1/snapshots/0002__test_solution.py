import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], True),
        ([5], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 3, 2, 4, 5], False),
        ([1, 2, 3, 4, 5, 6, 7], True),
        ([1, 3, 2, 4, 5, 6, 7], False),
        ([1, 2, 2, 3, 3, 4], True),
        ([1, 2, 2, 2, 3, 4], False),
        ([2, 2, 1], False),
        ([4, 4, 4], False),
    ],
)
def test_is_sorted(values, expected):
    assert is_sorted(values) is expected


def test_is_sorted_does_not_modify_input():
    values = [1, 2, 2, 3]
    original = values.copy()

    is_sorted(values)

    assert values == original
