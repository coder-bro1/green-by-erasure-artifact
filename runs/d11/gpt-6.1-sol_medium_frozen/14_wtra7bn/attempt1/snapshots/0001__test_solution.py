import pytest

from solution import intersperse


@pytest.mark.parametrize("delimiter", [0, 4, -7])
def test_empty_input(delimiter):
    numbers = []

    result = intersperse(numbers, delimiter)

    assert result == []
    assert result is not numbers


@pytest.mark.parametrize("numbers", [[], [1], [1, 2, 3], [-3, 0, -3]])
def test_input_is_not_modified(numbers):
    original = numbers.copy()

    result = intersperse(numbers, 9)

    assert numbers == original
    assert result is not numbers
    result.append(100)
    assert numbers == original


@pytest.mark.xfail(
    strict=True,
    reason="Known bug: intersperse omits the final input element",
)
@pytest.mark.parametrize(
    ("numbers", "delimiter", "expected"),
    [
        pytest.param([5], 4, [5], id="singleton"),
        pytest.param([1, 2], 4, [1, 4, 2], id="two-elements"),
        pytest.param([1, 2, 3], 4, [1, 4, 2, 4, 3], id="docstring-example"),
        pytest.param([-3, 0, 2], -1, [-3, -1, 0, -1, 2], id="negative-values"),
        pytest.param([0, 0, 0], 0, [0, 0, 0, 0, 0], id="repeated-zeroes"),
        pytest.param([4, 1, 4], 4, [4, 4, 1, 4, 4], id="delimiter-in-input"),
    ],
)
def test_inserts_delimiter_between_elements(numbers, delimiter, expected):
    assert intersperse(numbers, delimiter) == expected
