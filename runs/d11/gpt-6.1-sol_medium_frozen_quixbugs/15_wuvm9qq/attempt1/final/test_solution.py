import pytest

from solution import mergesort


def test_empty_list_returns_empty_list():
    assert mergesort([]) == []


def test_empty_list_is_not_modified():
    values = []
    mergesort(values)
    assert values == []


@pytest.mark.xfail(
    strict=True,
    raises=RecursionError,
    reason="mergesort lacks a singleton base case and recurses indefinitely",
)
@pytest.mark.parametrize(
    "values, expected",
    [
        ([7], [7]),
        ([1, 2], [1, 2]),
        ([2, 1], [1, 2]),
        ([3, 1, 2], [1, 2, 3]),
        ([4, 3, 2, 1], [1, 2, 3, 4]),
        ([5, 5, 5], [5, 5, 5]),
        ([3, 1, 3, 2, 1], [1, 1, 2, 3, 3]),
        ([0, -3, 2, -1, 0], [-3, -1, 0, 0, 2]),
        ([10**30, -(10**30), 0], [-(10**30), 0, 10**30]),
        (list(range(32, -1, -1)), list(range(33))),
    ],
    ids=[
        "singleton",
        "sorted-pair",
        "reversed-pair",
        "odd-length",
        "even-length",
        "equal-elements",
        "duplicates",
        "negative-and-zero",
        "large-integers",
        "longer-list",
    ],
)
def test_sorts_without_modifying_input(values, expected):
    original = values.copy()
    try:
        result = mergesort(values)
    finally:
        assert values == original
    assert result == expected
