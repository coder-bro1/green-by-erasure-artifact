import pytest

from solution import sort_numbers


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("", ""),
        ("zero", "zero"),
        ("one two three", "one two three"),
        ("one two two three", "one two two three"),
        ("one  two   three", "one two three"),
    ],
)
def test_sort_numbers_for_already_ordered_inputs(numbers, expected):
    assert sort_numbers(numbers) == expected
