import pytest

from solution import will_it_fly


# Docstring examples
@pytest.mark.parametrize(
    "q, w, expected",
    [
        ([1, 2], 5, False),
        ([3, 2, 3], 1, False),
        ([3, 2, 3], 9, True),
        ([3], 5, True),
    ],
)
def test_docstring_examples(q, w, expected):
    assert will_it_fly(q, w) is expected


def test_sum_equal_to_weight_flies():
    # "less than or equal" -> boundary must fly
    assert will_it_fly([3, 2, 3], 8) is True


def test_sum_one_over_weight_does_not_fly():
    assert will_it_fly([3, 2, 3], 7) is False


def test_unbalanced_and_too_heavy():
    assert will_it_fly([1, 2, 3], 1) is False


def test_unbalanced_but_light():
    assert will_it_fly([1, 2, 3], 100) is False


def test_even_length_palindrome():
    assert will_it_fly([1, 2, 2, 1], 6) is True


def test_even_length_non_palindrome():
    assert will_it_fly([1, 2, 1, 2], 6) is False


def test_mismatch_only_in_middle_pair():
    assert will_it_fly([1, 2, 3, 1], 100) is False


def test_long_palindrome():
    q = [5, 4, 3, 2, 1, 2, 3, 4, 5]
    assert will_it_fly(q, sum(q)) is True
    assert will_it_fly(q, sum(q) - 1) is False


def test_empty_list_flies():
    # Empty list is trivially palindromic and weighs 0.
    assert will_it_fly([], 0) is True
    assert will_it_fly([], 10) is True


def test_single_element_too_heavy():
    assert will_it_fly([6], 5) is False


def test_single_element_equal_weight():
    assert will_it_fly([5], 5) is True


def test_zero_weight_with_zeros():
    assert will_it_fly([0, 0, 0], 0) is True


def test_negative_weight_limit():
    assert will_it_fly([], -1) is False
    assert will_it_fly([1], -1) is False


def test_negative_elements():
    assert will_it_fly([-1, 2, -1], 0) is True
    assert will_it_fly([-1, 2, -2], 0) is False


def test_float_weight():
    assert will_it_fly([1, 1], 2.5) is True
    assert will_it_fly([1, 1], 1.5) is False


def test_does_not_mutate_input():
    q = [3, 2, 3]
    will_it_fly(q, 9)
    assert q == [3, 2, 3]
