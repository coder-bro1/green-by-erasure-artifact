import pytest

from solution import select_words

BUG = ("select_words counts vowels instead of consonants: the loop increments "
       "n_consonants when a letter IS in 'aeiou'")


# --- Docstring examples (all fail due to the vowel/consonant inversion) ---

@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_mary_4():
    assert select_words("Mary had a little lamb", 4) == ["little"]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_mary_3():
    assert select_words("Mary had a little lamb", 3) == ["Mary", "lamb"]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_simple_white_space():
    assert select_words("simple white space", 2) == []


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_hello_world():
    assert select_words("Hello world", 4) == ["world"]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_uncle_sam():
    assert select_words("Uncle sam", 3) == ["Uncle"]


# --- Additional spec tests ---

@pytest.mark.xfail(strict=True, reason=BUG)
def test_zero_consonants_selects_all_vowel_words():
    assert select_words("a e I ou", 0) == ["a", "e", "I", "ou"]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_uppercase_consonants_counted():
    assert select_words("BCD bcd xyz", 3) == ["BCD", "bcd", "xyz"]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_y_is_consonant():
    # "my" has 2 consonants (m, y)
    assert select_words("my", 2) == ["my"]


@pytest.mark.xfail(strict=True, reason=BUG)
def test_no_match_returns_empty():
    assert select_words("aaa eee", 1) == []


@pytest.mark.xfail(strict=True, reason=BUG)
def test_order_and_duplicates_preserved():
    assert select_words("cat dog cat", 2) == ["cat", "dog", "cat"]


# --- Cases where current behavior matches the spec ---

def test_empty_string():
    assert select_words("", 3) == []


def test_empty_string_zero():
    assert select_words("", 0) == []


def test_whitespace_only():
    assert select_words("   ", 0) == []


def test_multiple_spaces_between_words():
    # vowel count == consonant count for these words, so the bug is masked
    assert select_words("abba   cede", 2) == ["abba", "cede"]


def test_returns_list():
    assert isinstance(select_words("hello", 1), list)
