import pytest

from solution import sort_numbers

WORDS = ['zero', 'one', 'two', 'three', 'four',
         'five', 'six', 'seven', 'eight', 'nine']


def test_docstring_example():
    assert sort_numbers('three one five') == 'one three five'


def test_empty_string():
    assert sort_numbers('') == ''


def test_single_word():
    assert sort_numbers('three') == 'three'


@pytest.mark.parametrize('word', WORDS)
def test_each_single_word(word):
    assert sort_numbers(word) == word


def test_already_sorted():
    assert sort_numbers('one two three') == 'one two three'


def test_reverse_order():
    assert sort_numbers(' '.join(reversed(WORDS))) == ' '.join(WORDS)


def test_mixed_order():
    assert sort_numbers('five zero four seven nine eight') == 'zero four five seven eight nine'


def test_duplicates_preserved():
    assert sort_numbers('six five four three two one zero') == 'zero one two three four five six'
    assert sort_numbers('two one two one') == 'one one two two'


def test_extra_spaces_ignored():
    assert sort_numbers('  three   one  ') == 'one three'


def test_alphabetical_order_is_not_used():
    # Alphabetically 'eight' < 'two', numerically 2 < 8.
    assert sort_numbers('eight two') == 'two eight'
