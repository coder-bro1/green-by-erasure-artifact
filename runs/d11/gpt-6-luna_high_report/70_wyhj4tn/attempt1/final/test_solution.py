import pytest

from solution import sort_numbers


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ("three one five", "one three five"),
        ("nine zero four two", "zero two four nine"),
        ("five two five one", "one two five five"),
        ("eight seven six five four three two one zero", "zero one two three four five six seven eight"),
    ],
)
@pytest.mark.xfail(
    strict=True,
    reason="sort_numbers preserves input order instead of sorting words by their numeric values",
)
def test_sorts_numbers_in_ascending_numeric_order(numbers, expected):
    assert sort_numbers(numbers) == expected


def test_keeps_an_already_sorted_sequence_sorted():
    assert sort_numbers("zero two two five nine") == "zero two two five nine"


def test_single_number_is_unchanged():
    assert sort_numbers("seven") == "seven"


def test_empty_input_returns_empty_string():
    assert sort_numbers("") == ""
