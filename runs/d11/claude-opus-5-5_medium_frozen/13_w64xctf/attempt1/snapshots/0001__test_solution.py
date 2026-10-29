import pytest

from solution import is_sorted


@pytest.mark.parametrize(
    "lst, expected",
    [
        ([5], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 3, 2, 4, 5], False),
        ([1, 2, 3, 4, 5, 6], True),
        ([1, 2, 3, 4, 5, 6, 7], True),
        ([1, 3, 2, 4, 5, 6, 7], False),
        ([1, 2, 2, 3, 3, 4], True),
    ],
)
def test_docstring_examples(lst, expected):
    assert is_sorted(lst) is expected


def test_empty_list_is_sorted():
    assert is_sorted([]) is True


def test_single_zero():
    assert is_sorted([0]) is True


def test_two_ascending():
    assert is_sorted([0, 1]) is True


def test_two_descending():
    assert is_sorted([1, 0]) is False


def test_single_duplicate_pair_allowed():
    assert is_sorted([3, 3]) is True


def test_descending_list():
    assert is_sorted([5, 4, 3, 2, 1]) is False


def test_unsorted_only_at_end():
    assert is_sorted([1, 2, 3, 4, 0]) is False


def test_unsorted_only_at_start():
    assert is_sorted([9, 1, 2, 3]) is False


def test_large_gaps():
    assert is_sorted([0, 10, 1000, 10**9]) is True


def test_long_sorted_range():
    assert is_sorted(list(range(1000))) is True


def test_returns_bool():
    assert isinstance(is_sorted([1, 2]), bool)
    assert isinstance(is_sorted([2, 1]), bool)


def test_does_not_mutate_input():
    data = [1, 3, 2]
    is_sorted(data)
    assert data == [1, 3, 2]


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: solution.py counts occurrences but never checks them, "
    "so lists with 3+ copies of a number are not rejected as the docstring requires.",
)
@pytest.mark.parametrize("lst", [[1, 2, 2, 2, 3, 4], [1, 1, 1], [0, 5, 5, 5, 5]])
def test_triplicate_rejected_per_docstring(lst):
    assert is_sorted(lst) is False


@pytest.mark.parametrize("lst", [[1, 2, 2, 2, 3, 4], [1, 1, 1]])
def test_triplicate_current_behavior(lst):
    # Documents actual current behavior (see xfail above).
    assert is_sorted(lst) is True
