import pytest

from solution import sort_numbers

WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def test_docstring_example():
    assert sort_numbers('three one five') == 'one three five'


def test_empty_string():
    assert sort_numbers('') == ''


@pytest.mark.parametrize("word", WORDS)
def test_single_word(word):
    assert sort_numbers(word) == word


def test_already_sorted():
    assert sort_numbers('zero one two') == 'zero one two'


def test_reverse_all():
    assert sort_numbers(' '.join(reversed(WORDS))) == ' '.join(WORDS)


def test_numeric_not_alphabetical_order():
    # Alphabetically 'eight' < 'five' < 'four' < 'nine', numerically different.
    assert sort_numbers('nine eight four five') == 'four five eight nine'


def test_duplicates_preserved():
    assert sort_numbers('five zero four seven nine eight') == 'zero four five seven eight nine'
    assert sort_numbers('six five four three two one zero') == 'zero one two three four five six'
    assert sort_numbers('two two one one') == 'one one two two'


def test_extra_spaces_ignored():
    assert sort_numbers('  three   one  five ') == 'one three five'


def test_only_spaces():
    assert sort_numbers('   ') == ''


def test_invalid_word_raises():
    with pytest.raises(KeyError):
        sort_numbers('one eleven')


def test_input_not_mutated_and_returns_str():
    s = 'three one'
    result = sort_numbers(s)
    assert isinstance(result, str)
    assert s == 'three one'
