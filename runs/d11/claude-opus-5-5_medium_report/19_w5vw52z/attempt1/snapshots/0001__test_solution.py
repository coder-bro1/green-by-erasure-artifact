import pytest

from solution import is_sorted

TRIPLICATE_REASON = (
    "solution.py builds count_digit but never checks it, so a number appearing "
    "3+ times is not rejected as the docstring requires"
)


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


@pytest.mark.xfail(strict=True, reason=TRIPLICATE_REASON)
def test_docstring_example_triplicate():
    assert is_sorted([1, 2, 2, 2, 3, 4]) is False


def test_empty_list():
    assert is_sorted([]) is True


def test_zero_allowed():
    assert is_sorted([0, 1, 2]) is True


def test_descending():
    assert is_sorted([5, 4, 3, 2, 1]) is False


def test_last_pair_unsorted():
    assert is_sorted([1, 2, 3, 5, 4]) is False


def test_single_pair_duplicate():
    assert is_sorted([1, 1]) is True


def test_duplicate_but_unsorted():
    assert is_sorted([2, 2, 1]) is False


def test_does_not_mutate_input():
    lst = [1, 3, 2]
    is_sorted(lst)
    assert lst == [1, 3, 2]


@pytest.mark.xfail(strict=True, reason=TRIPLICATE_REASON)
def test_triplicate_only_elements():
    assert is_sorted([3, 3, 3]) is False


@pytest.mark.xfail(strict=True, reason=TRIPLICATE_REASON)
def test_triplicate_at_end():
    assert is_sorted([1, 2, 4, 4, 4]) is False


@pytest.mark.xfail(strict=True, reason=TRIPLICATE_REASON)
def test_quadruplicate():
    assert is_sorted([1, 1, 1, 1]) is False
