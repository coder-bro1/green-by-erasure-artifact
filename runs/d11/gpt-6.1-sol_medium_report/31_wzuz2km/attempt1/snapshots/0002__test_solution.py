import pytest

from solution import intersperse


@pytest.mark.parametrize("delimiter", [4, 0, -7])
def test_empty_list(delimiter):
    assert intersperse([], delimiter) == []


@pytest.mark.xfail(
    strict=True,
    reason="Docstring requires preserving all input elements; intersperse omits the final element.",
)
@pytest.mark.parametrize(
    "numbers, delimiter, expected",
    [
        pytest.param([1, 2, 3], 4, [1, 4, 2, 4, 3], id="docstring-example"),
        pytest.param([7], 4, [7], id="single-element"),
        pytest.param([1, 2], 9, [1, 9, 2], id="two-elements"),
        pytest.param([1, 2, 3, 4], 0, [1, 0, 2, 0, 3, 0, 4], id="zero-delimiter"),
        pytest.param([-3, 0, 5], -1, [-3, -1, 0, -1, 5], id="negative-values"),
        pytest.param([2, 2, 2], 2, [2, 2, 2, 2, 2], id="repeated-values"),
        pytest.param([0, 0], 5, [0, 5, 0], id="zero-elements"),
        pytest.param([10**30, -(10**30)], 8, [10**30, 8, -(10**30)], id="large-integers"),
    ],
)
def test_inserts_delimiter_between_elements(numbers, delimiter, expected):
    assert intersperse(numbers, delimiter) == expected


@pytest.mark.parametrize("numbers", [[], [7], [1, 2, 3]])
def test_does_not_modify_input(numbers):
    original = numbers.copy()
    result = intersperse(numbers, 4)

    assert numbers == original
    assert result is not numbers
    result.append(99)
    assert numbers == original
