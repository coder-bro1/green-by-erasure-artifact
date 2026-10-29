import pytest

from solution import sort_numbers

NOT_SORTED = (
    "sort_numbers never sorts: value_map is built but unused, and the function "
    "only returns the input tokens in their original order"
)


def test_empty_string():
    assert sort_numbers('') == ''


def test_single_word():
    assert sort_numbers('three') == 'three'


def test_already_sorted_input():
    assert sort_numbers('zero one two three four five six seven eight nine') == \
        'zero one two three four five six seven eight nine'


def test_already_sorted_with_duplicates():
    assert sort_numbers('one one two') == 'one one two'


def test_extra_spaces_are_dropped():
    assert sort_numbers('  one   two  ') == 'one two'


@pytest.mark.xfail(strict=True, reason=NOT_SORTED)
def test_docstring_example():
    assert sort_numbers('three one five') == 'one three five'


@pytest.mark.xfail(strict=True, reason=NOT_SORTED)
def test_reverse_order():
    assert sort_numbers('nine eight seven six five four three two one zero') == \
        'zero one two three four five six seven eight nine'


@pytest.mark.xfail(strict=True, reason=NOT_SORTED)
def test_unsorted_with_duplicates():
    assert sort_numbers('five zero five one') == 'zero one five five'


@pytest.mark.xfail(strict=True, reason=NOT_SORTED)
def test_numeric_not_alphabetical_order():
    # Alphabetical order would give 'eight five four'
    assert sort_numbers('four eight five') == 'four five eight'


@pytest.mark.xfail(strict=True, reason=NOT_SORTED)
def test_two_words_swapped():
    assert sort_numbers('two one') == 'one two'
