import pytest

from solution import intersperse


@pytest.mark.parametrize(
    ("numbers", "delimiter", "expected"),
    [
        pytest.param([], 4, [], id="empty-docstring-example"),
        pytest.param([1, 2, 3], 4, [1, 4, 2, 4, 3], id="docstring-example"),
        pytest.param([7], 4, [7], id="single-element"),
        pytest.param([1, 2], 9, [1, 9, 2], id="two-elements"),
        pytest.param([1, 2, 3, 4], 0, [1, 0, 2, 0, 3, 0, 4], id="zero-delimiter"),
        pytest.param([-3, -2, -1], -9, [-3, -9, -2, -9, -1], id="negative-values"),
        pytest.param([0, -1, 2], 3, [0, 3, -1, 3, 2], id="mixed-signs"),
        pytest.param([5, 5, 5], 5, [5, 5, 5, 5, 5], id="all-values-equal"),
        pytest.param([4, 1, 4], 4, [4, 4, 1, 4, 4], id="delimiter-in-input"),
        pytest.param([3, 1, 3, 2], 8, [3, 8, 1, 8, 3, 8, 2], id="preserve-order"),
        pytest.param(
            [10**100, -(10**100)],
            10**101,
            [10**100, 10**101, -(10**100)],
            id="large-integers",
        ),
    ],
)
def test_intersperse(numbers, delimiter, expected):
    assert intersperse(numbers, delimiter) == expected


def test_intersperse_does_not_modify_input():
    numbers = [1, 2, 3]
    original = numbers.copy()

    intersperse(numbers, 4)

    assert numbers == original
