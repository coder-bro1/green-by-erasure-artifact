import pytest

from solution import is_happy

BUG = (
    "is_happy only rejects a window when all three characters are equal; "
    "the docstring requires every 3 consecutive letters to be distinct, so "
    "a window with just two equal characters must also return False"
)


@pytest.mark.parametrize("s", ["", "a", "aa", "ab"])
def test_too_short_is_not_happy(s):
    assert is_happy(s) is False


@pytest.mark.parametrize("s", ["abc", "adb", "abcd", "abcabc", "xyzxyz", "iopaxpoi"])
def test_happy_strings(s):
    assert is_happy(s) is True


@pytest.mark.parametrize("s", ["aaa", "abbbc", "xaaay"])
def test_three_identical_in_a_row_not_happy(s):
    assert is_happy(s) is False


def test_docstring_example_a():
    assert is_happy("a") is False


def test_docstring_example_aa():
    assert is_happy("aa") is False


def test_docstring_example_abcd():
    assert is_happy("abcd") is True


def test_docstring_example_adb():
    assert is_happy("adb") is True


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example_aabb():
    assert is_happy("aabb") is False


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example_xyy():
    assert is_happy("xyy") is False


@pytest.mark.xfail(strict=True, reason=BUG)
def test_adjacent_duplicate_at_start():
    assert is_happy("aab") is False


@pytest.mark.xfail(strict=True, reason=BUG)
def test_first_and_third_equal():
    assert is_happy("aba") is False


@pytest.mark.xfail(strict=True, reason=BUG)
def test_duplicate_late_in_long_string():
    assert is_happy("abcdefgg") is False
