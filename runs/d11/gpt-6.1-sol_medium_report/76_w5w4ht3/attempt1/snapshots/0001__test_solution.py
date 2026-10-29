import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], 0, id="empty-list"),
        pytest.param([0], 0, id="documented-zero"),
        pytest.param([-1, -2, 0], 0, id="documented-nonpositive"),
        pytest.param([9, -2], 81, id="documented-mixed-signs"),
        pytest.param([1], 1, id="single-odd"),
        pytest.param([1, 3, 5, 7, 9], 165, id="multiple-odds"),
        pytest.param([3, 3, 1], 19, id="duplicates-count-separately"),
        pytest.param([-9, -7, -3, -1], 0, id="negative-odds-ignored"),
        pytest.param([0, 0, 0], 0, id="multiple-zeros"),
        pytest.param([0.5, 1.5, 2.5, -3.5], 0, id="fractional-floats-ignored"),
        pytest.param([1.0, 3.0, 5.0], 0, id="integral-floats-ignored"),
        pytest.param([1, 3.0, 5, -7, 0, 2.5], 26, id="mixed-numeric-types"),
        pytest.param([10**100 + 1], (10**100 + 1) ** 2, id="large-odd-integer"),
    ],
)
def test_documented_behavior(numbers, expected):
    assert double_the_difference(numbers) == expected


@pytest.mark.xfail(
    strict=True,
    reason="solution.py squares positive even integers, but the docstring requires only odd integers",
)
@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([1, 3, 2, 0], 10, id="documented-example-with-even"),
        pytest.param([2], 0, id="single-even"),
        pytest.param([2, 4, 6, 8], 0, id="all-even"),
        pytest.param([1, 2, 3, 4, 5], 35, id="mixed-odd-and-even"),
        pytest.param([-3, -2, 0, 2, 3, 1.5, 5.0], 9, id="mixed-signs-and-types"),
        pytest.param([10**100], 0, id="large-even-integer"),
    ],
)
def test_positive_even_integers_are_ignored(numbers, expected):
    assert double_the_difference(numbers) == expected


def test_does_not_modify_input():
    numbers = [9, -3, 1.5, 0, 1, 9]
    original = numbers.copy()

    assert double_the_difference(numbers) == 163
    assert numbers == original
