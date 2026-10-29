import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([0], 0, id="zero"),
        pytest.param([-1, -2, 0], 0, id="nonpositive-integers"),
        pytest.param([9, -2], 81, id="odd-and-negative"),
        pytest.param([1], 1, id="one"),
        pytest.param([1, 3, 5, 7, 9], 165, id="positive-odds"),
        pytest.param([3, 3, 3], 27, id="duplicates-counted"),
        pytest.param([-3, 0, 1, 3, -5], 10, id="mixed-signs"),
        pytest.param([1.0, 3.0, 2.5, -1.5, 0.0], 0, id="floats-ignored"),
        pytest.param([1, 3.0, 5, -7, 2.5], 26, id="integers-and-floats"),
        pytest.param([10**100 + 1], (10**100 + 1) ** 2, id="large-odd"),
    ],
)
def test_sum_of_squares_of_nonnegative_odd_integers(numbers, expected):
    result = double_the_difference(numbers)

    assert result == expected
    assert type(result) is int


def test_input_list_is_not_modified():
    numbers = [5, -3, 1.5, 0, 1, 5]
    original = numbers.copy()

    assert double_the_difference(numbers) == 51
    assert numbers == original


@pytest.mark.xfail(
    strict=True,
    reason="Known defect: solution.py includes positive even integers.",
)
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([2], 0, id="single-even"),
        pytest.param([2, 4, 6], 0, id="only-evens"),
        pytest.param([1, 3, 2, 0], 10, id="docstring-example"),
    ],
)
def test_positive_even_integers_are_ignored(numbers, expected):
    assert double_the_difference(numbers) == expected
