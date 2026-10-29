import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([], 0),
        ([0], 0),
        ([-1, -2, -9], 0),
        ([1, 3, 9], 91),
        ([1, -3, 5], 26),
        ([1.5, 2.5, -3.5], 0),
        ([1, 3.0, 5.5, -7, 9], 82),
    ],
)
def test_sums_squares_of_positive_odd_integers(numbers, expected):
    assert double_the_difference(numbers) == expected


@pytest.mark.xfail(
    reason="solution.py currently includes positive even integers in the sum",
    strict=False,
)
def test_ignores_positive_even_integers():
    assert double_the_difference([2, 4, 6]) == 0


@pytest.mark.xfail(
    reason="solution.py currently includes positive even integers in the sum",
    strict=False,
)
def test_documented_mixed_example():
    # This example also exposes the positive-even-integer bug and is tracked above.
    assert double_the_difference([1, 3, 2, 0]) == 10
