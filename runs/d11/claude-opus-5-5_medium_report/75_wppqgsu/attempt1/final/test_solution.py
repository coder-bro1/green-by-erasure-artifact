import pytest

from solution import longest

BUG = ("longest() compares len(s) > maxlen, which is never true, so it falls "
       "through and returns None for every non-empty list")


def test_empty_list_returns_none():
    assert longest([]) is None


@pytest.mark.xfail(strict=True, reason=BUG)
def test_all_same_length_returns_first():
    assert longest(['a', 'b', 'c']) == 'a'


@pytest.mark.xfail(strict=True, reason=BUG)
def test_increasing_lengths_returns_last():
    assert longest(['a', 'bb', 'ccc']) == 'ccc'


@pytest.mark.xfail(strict=True, reason=BUG)
def test_single_element():
    assert longest(['hello']) == 'hello'


@pytest.mark.xfail(strict=True, reason=BUG)
def test_longest_in_middle():
    assert longest(['x', 'yyyy', 'zz']) == 'yyyy'


@pytest.mark.xfail(strict=True, reason=BUG)
def test_tie_for_longest_returns_first_of_them():
    assert longest(['a', 'abc', 'xyz', 'b']) == 'abc'


@pytest.mark.xfail(strict=True, reason=BUG)
def test_single_empty_string():
    assert longest(['']) == ''
