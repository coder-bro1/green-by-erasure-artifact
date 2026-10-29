import pytest

from solution import most_frequent_letters


def test_doc_example_single_winner():
    assert most_frequent_letters('p q p') == {'p': 2}


def test_doc_example_tie_all_once():
    assert most_frequent_letters('z y') == {'z': 1, 'y': 1}


def test_single_letter():
    assert most_frequent_letters('a') == {'a': 1}


def test_same_letter_repeated():
    assert most_frequent_letters('b b b b') == {'b': 4}


def test_tie_at_maximum_excludes_lower_counts():
    assert most_frequent_letters('a b a b c') == {'a': 2, 'b': 2}


def test_clear_winner_among_many():
    assert most_frequent_letters('x y z x y x') == {'x': 3}


def test_all_distinct_letters_all_included():
    text = ' '.join('abcdefghij')
    assert most_frequent_letters(text) == {c: 1 for c in 'abcdefghij'}


def test_winner_not_first():
    assert most_frequent_letters('a b c c') == {'c': 2}


def test_returns_new_dict_each_call():
    first = most_frequent_letters('a a')
    first['zzz'] = 99
    assert most_frequent_letters('a a') == {'a': 2}


@pytest.mark.xfail(
    strict=True,
    reason="Bug in solution.py: best starts at 1, so the empty string's single "
           "'' part is counted and {'': 1} is returned instead of {}.",
)
def test_empty_string_gives_empty_dict():
    assert most_frequent_letters('') == {}
