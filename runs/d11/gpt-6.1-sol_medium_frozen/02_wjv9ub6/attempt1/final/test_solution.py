import pytest

from solution import sort_numbers


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("   ", "", id="spaces-only"),
        pytest.param("zero", "zero", id="single-zero"),
        pytest.param("nine", "nine", id="single-nine"),
        pytest.param("five five five", "five five five", id="identical-values"),
        pytest.param("zero one two", "zero one two", id="already-sorted"),
        pytest.param("  one  two   three  ", "one two three", id="extra-spaces"),
        pytest.param("three one five", "one three five", id="docstring-example"),
        pytest.param("nine zero", "zero nine", id="boundary-values"),
        pytest.param("two one two zero one", "zero one one two two", id="duplicates"),
        pytest.param("  five   zero  two ", "zero two five", id="unsorted-extra-spaces"),
        pytest.param(
            "nine eight seven six five four three two one zero",
            "zero one two three four five six seven eight nine",
            id="all-values-reversed",
        ),
        pytest.param(
            "eight five four nine one seven six three two zero",
            "zero one two three four five six seven eight nine",
            id="numeric-rather-than-alphabetical-order",
        ),
    ],
)
def test_sort_numbers(numbers, expected):
    assert sort_numbers(numbers) == expected


@pytest.mark.parametrize(
    "number",
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],
)
def test_each_valid_number_is_preserved(number):
    assert sort_numbers(number) == number
