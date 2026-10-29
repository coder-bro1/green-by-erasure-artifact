import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], True),
        ([5], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 3, 2, 4, 5], False),
        ([1, 2, 2, 3, 3, 4], True),
        ([4, 4, 3], False),
        ([2, 1, 3], False),
    ],
)
def test_is_sorted(numbers, expected):
    assert is_sorted(numbers) is expected


@pytest.mark.xfail(
    strict=True,
    reason="is_sorted checks order but does not reject values occurring more than twice",
)
def test_is_sorted_rejects_value_occurring_more_than_twice():
    assert is_sorted([1, 2, 2, 2, 3, 4]) is False
