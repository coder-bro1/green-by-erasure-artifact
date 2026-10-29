import pytest

from solution import order_number_words


def test_docstring_example():
    assert order_number_words('nine two six') == 'two six nine'


def test_empty_string():
    assert order_number_words('') == ''


def test_single_word():
    assert order_number_words('five') == 'five'


def test_already_sorted():
    assert order_number_words('zero one two') == 'zero one two'


def test_reverse_order():
    assert order_number_words('nine eight seven') == 'seven eight nine'


def test_all_words_shuffled():
    phrase = 'three nine zero five one eight two seven four six'
    expected = 'zero one two three four five six seven eight nine'
    assert order_number_words(phrase) == expected


def test_duplicates_kept():
    assert order_number_words('two one two one') == 'one one two two'


def test_extra_spaces_collapsed():
    assert order_number_words('  six   three  ') == 'three six'


def test_only_spaces():
    assert order_number_words('   ') == ''


@pytest.mark.parametrize(
    'phrase, expected',
    [
        ('one zero', 'zero one'),
        ('four three', 'three four'),
        ('eight seven six', 'six seven eight'),
    ],
)
def test_pairs_and_triples(phrase, expected):
    assert order_number_words(phrase) == expected
