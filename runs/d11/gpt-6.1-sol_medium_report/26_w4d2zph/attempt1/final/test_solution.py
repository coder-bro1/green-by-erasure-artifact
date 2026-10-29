import math

import pytest

from solution import double_the_difference


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param([1, 3, 2, 0], 10, id="docstring-mixed"),
        pytest.param([-1, -2, 0], 0, id="docstring-negatives"),
        pytest.param([9, -2], 81, id="docstring-positive-and-negative"),
        pytest.param([0], 0, id="docstring-zero"),
        pytest.param([], 0, id="empty"),
        pytest.param([1], 1, id="smallest-positive-odd"),
        pytest.param([1, 3, 5, 7], 84, id="odd-integers"),
        pytest.param([2, 4, 6, 8], 0, id="even-integers"),
        pytest.param([-1, -3, -5], 0, id="negative-odd-integers"),
        pytest.param([3, 3, 3], 27, id="duplicates-counted"),
        pytest.param([1.0, 3.0, 5.0], 0, id="float-values-ignored"),
        pytest.param([0.5, 1.5, 2.5, -3.5], 0, id="fractions-ignored"),
        pytest.param([3, math.nan], 9, id="nan-ignored"),
        pytest.param([1, 2.5, -3, 4, 5, 7.0, 0], 26, id="mixed-types"),
        pytest.param([10**100 + 1, 10**100], (10**100 + 1) ** 2,
                     id="large-integers-exact"),
    ],
)
def test_documented_behavior(numbers, expected):
    assert double_the_difference(numbers) == expected


def test_input_list_is_unchanged():
    numbers = [5, -3, 1.5, 2, 1]
    original = numbers.copy()

    assert double_the_difference(numbers) == 26
    assert numbers == original


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The docstring requires ignoring non-integers, but the implementation "
        "accepts positive floats whose string representation has no decimal point."
    ),
)
@pytest.mark.parametrize(
    "non_integer",
    [
        pytest.param(1e-5, id="scientific-notation-fraction"),
        pytest.param(math.inf, id="positive-infinity"),
    ],
)
def test_non_integer_numbers_are_ignored(non_integer):
    assert double_the_difference([3, non_integer]) == 9
