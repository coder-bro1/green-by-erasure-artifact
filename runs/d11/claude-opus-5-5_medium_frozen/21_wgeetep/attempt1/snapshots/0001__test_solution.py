import pytest

from solution import double_the_difference


# ---- Behaviour the current implementation satisfies ----

def test_empty_list_returns_zero():
    assert double_the_difference([]) == 0


def test_zero_only():
    assert double_the_difference([0]) == 0


def test_all_negative_or_zero():
    assert double_the_difference([-1, -2, 0]) == 0


def test_negatives_ignored():
    assert double_the_difference([9, -2]) == 81
    assert double_the_difference([-3, -5, 7]) == 49


def test_odd_positive_integers_squared_and_summed():
    assert double_the_difference([1, 3, 5]) == 1 + 9 + 25


def test_floats_ignored():
    assert double_the_difference([0.1, 0.2, 0.3]) == 0
    assert double_the_difference([5.0, 3]) == 9
    assert double_the_difference([-10.5, 2.5, 3]) == 9


def test_does_not_mutate_input():
    data = [1, 3, -1, 2.5]
    double_the_difference(data)
    assert data == [1, 3, -1, 2.5]


def test_large_odd_range():
    lst = list(range(-99, 100, 2))  # odd numbers only
    expected = sum(i ** 2 for i in lst if i > 0)
    assert double_the_difference(lst) == expected


def test_current_behaviour_includes_even_numbers():
    # Documents actual behaviour: the implementation does not filter out
    # even numbers, contrary to its docstring.
    assert double_the_difference([1, 3, 2, 0]) == 14
    assert double_the_difference([2, 4]) == 20


# ---- Docstring spec that the implementation violates ----

@pytest.mark.xfail(reason="solution.py does not exclude even numbers", strict=True)
def test_spec_docstring_example_even_numbers_excluded():
    assert double_the_difference([1, 3, 2, 0]) == 10


@pytest.mark.xfail(reason="solution.py does not exclude even numbers", strict=True)
def test_spec_only_evens_returns_zero():
    assert double_the_difference([2, 4, 6]) == 0
