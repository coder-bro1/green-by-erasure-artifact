import pytest

from solution import longest


def test_empty_list_returns_none():
    assert longest([]) is None


def test_all_same_length_returns_first():
    assert longest(['a', 'b', 'c']) == 'a'


def test_increasing_lengths_returns_last():
    assert longest(['a', 'bb', 'ccc']) == 'ccc'


def test_longest_in_middle():
    assert longest(['x', 'yyyy', 'zz']) == 'yyyy'


def test_tie_returns_first_of_longest():
    assert longest(['ab', 'cde', 'fgh', 'i']) == 'cde'


def test_single_element():
    assert longest(['hello']) == 'hello'


def test_single_empty_string():
    assert longest(['']) == ''


def test_empty_strings_and_nonempty():
    assert longest(['', 'a', '']) == 'a'


def test_does_not_mutate_input():
    data = ['a', 'bbb', 'cc']
    longest(data)
    assert data == ['a', 'bbb', 'cc']
