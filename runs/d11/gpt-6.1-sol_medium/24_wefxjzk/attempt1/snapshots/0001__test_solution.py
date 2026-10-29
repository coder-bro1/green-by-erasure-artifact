import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([], 0, id="empty"),
        pytest.param([1, 3, 2, 0], 10, id="documented-mixed-example"),
        pytest.param([-1, -2, 0], 0, id="documented-nonpositive-example"),
        pytest.param([9, -2], 81, id="documented-positive-and-negative"),
        pytest.param([0], 0, id="zero"),
        pytest.param([2, 4, 6, 8], 0, id="positive-even-integers"),
        pytest.param([1, 3, 5, 7], 84, id="positive-odd-integers"),
        pytest.param([-1, -3, -5], 0, id="negative-odd-integers"),
        pytest.param([1.5, 2.5, -3.5], 0, id="fractional-floats"),
        pytest.param([1.0, 3.0, 5.0], 0, id="integer-valued-floats"),
        pytest.param([1e20, 1e-7], 0, id="scientific-notation-floats"),
        pytest.param([3, 3, 3], 27, id="repeated-values"),
        pytest.param([-7, -2, 0, 2, 3, 4, 5, 7.0, 9.5], 34, id="mixed-types-and-signs"),
        pytest.param([10**30 + 1, 10**30], (10**30 + 1) ** 2, id="large-integers"),
    ],
)
def test_double_the_difference(numbers, expected):
    assert double_the_difference(numbers) == expected


def test_double_the_difference_does_not_modify_input():
    numbers = [5, -3, 2, 1.5, 0, 1]
    original = numbers.copy()

    assert double_the_difference(numbers) == 26
    assert numbers == original
