import pytest
from solution import can_lift


@pytest.mark.parametrize("load, limit, expected", [
    ([4, 1, 4], 10, True),    # docstring: palindrome, sum 9 <= 10
    ([4, 1, 4], 8, False),    # docstring: sum over limit
    ([2, 5], 9, False),       # docstring: not a palindrome
    ([6], 7, True),           # docstring: single element
])
def test_docstring_examples(load, limit, expected):
    assert can_lift(load, limit) is expected


def test_empty_load_is_liftable():
    assert can_lift([], 0) is True


def test_sum_exactly_at_limit():
    assert can_lift([3, 3], 6) is True


def test_sum_one_over_limit():
    assert can_lift([3, 3], 5) is False


def test_even_length_palindrome():
    assert can_lift([1, 2, 2, 1], 100) is True


def test_odd_length_palindrome():
    assert can_lift([1, 2, 3, 2, 1], 9) is True


def test_non_palindrome_under_limit():
    assert can_lift([1, 2, 3], 100) is False


def test_non_palindrome_with_matching_ends():
    assert can_lift([1, 2, 3, 1], 100) is False


def test_single_element_over_limit():
    assert can_lift([8], 7) is False


def test_negative_limit_with_negative_values():
    assert can_lift([-2, -2], -4) is True
    assert can_lift([-2, -2], -5) is False


def test_does_not_mutate_input():
    load = [4, 1, 4]
    can_lift(load, 10)
    assert load == [4, 1, 4]
