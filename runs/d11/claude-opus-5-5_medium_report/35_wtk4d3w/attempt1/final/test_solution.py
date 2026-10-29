import pytest

from solution import longest


def test_empty_list_returns_none():
    assert longest([]) is None


def test_docstring_all_same_length_returns_first():
    assert longest(['a', 'b', 'c']) == 'a'


def test_docstring_increasing_lengths():
    assert longest(['a', 'bb', 'ccc']) == 'ccc'


def test_single_element():
    assert longest(['hello']) == 'hello'


def test_single_empty_string():
    assert longest(['']) == ''


def test_all_empty_strings_returns_first():
    strings = ['', '', '']
    result = longest(strings)
    assert result == ''
    assert result is strings[0]


def test_longest_in_middle():
    assert longest(['ab', 'abcd', 'abc']) == 'abcd'


def test_longest_at_start():
    assert longest(['zzzz', 'a', 'bb']) == 'zzzz'


def test_tie_returns_first_of_tied():
    assert longest(['x', 'abc', 'def', 'gh', 'ijk']) == 'abc'


def test_tie_returns_first_object_identity():
    first = 'ab' + 'cd'
    second = 'ef' + 'gh'
    assert longest(['a', first, second]) is first


def test_whitespace_counts_toward_length():
    assert longest(['abc', '    ']) == '    '


def test_unicode_length_by_code_points():
    assert longest(['ab', 'äöü']) == 'äöü'


def test_does_not_mutate_input():
    strings = ['b', 'aaa', 'cc']
    copy = list(strings)
    longest(strings)
    assert strings == copy


@pytest.mark.parametrize(
    "strings, expected",
    [
        (['x', 'y', 'z'], 'x'),
        (['x', 'yyyyy', 'z'], 'yyyyy'),
        (['kitten', 'sitting', 'mitten'], 'sitting'),
        (['abc', 'ab', 'a'], 'abc'),
    ],
)
def test_parametrized(strings, expected):
    assert longest(strings) == expected
