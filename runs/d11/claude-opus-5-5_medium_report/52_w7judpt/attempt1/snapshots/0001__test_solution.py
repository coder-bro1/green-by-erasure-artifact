import pytest

from solution import file_name_check


# --- Docstring examples ---

def test_docstring_valid_example():
    assert file_name_check("example.txt") == "Yes"


def test_docstring_starts_with_digit():
    assert file_name_check("1example.dll") == "No"


# --- Valid names ---

@pytest.mark.parametrize("name", [
    "example.txt",
    "example.exe",
    "example.dll",
    "a.txt",
    "Z.exe",
    "My_File.dll",
    "abc123.txt",       # exactly three digits
    "a1b2c3.exe",       # three digits scattered
    "K-dot.dll",
    "a b.txt",
])
def test_valid_names(name):
    assert file_name_check(name) == "Yes"


# --- Digit count ---

@pytest.mark.parametrize("name", [
    "abc1234.txt",
    "a1b2c3d4.exe",
    "x0000.dll",
])
def test_more_than_three_digits(name):
    assert file_name_check(name) == "No"


# --- Dot count ---

@pytest.mark.parametrize("name", [
    "example",           # no dot
    "example.txt.txt",   # two dots
    "a..txt",
    "exampletxt",
    "",
    "...",
])
def test_not_exactly_one_dot(name):
    assert file_name_check(name) == "No"


# --- Prefix rules ---

@pytest.mark.parametrize("name", [
    ".txt",       # empty prefix
    "1abc.txt",
    "_abc.exe",
    " abc.dll",
    "-abc.txt",
])
def test_bad_prefix(name):
    assert file_name_check(name) == "No"


# --- Suffix rules (solution.py never checks the extension) ---

@pytest.mark.xfail(strict=True, reason="solution.py never checks that the suffix is one of txt/exe/dll")
@pytest.mark.parametrize("name", [
    "example.pdf",
    "example.",        # empty suffix
    "example.TXT",     # case-sensitive per docstring list
    "example.txtx",
    "example.tx",
    "example. txt",
])
def test_bad_suffix(name):
    assert file_name_check(name) == "No"


# --- Latin-letter requirement (isalpha accepts any Unicode letter) ---

@pytest.mark.xfail(strict=True, reason="solution.py uses str.isalpha(), which accepts non-Latin letters")
@pytest.mark.parametrize("name", [
    "école.txt",   # e-acute
    "αlpha.txt",   # Greek alpha
    "фile.exe",    # Cyrillic ef
])
def test_non_latin_first_letter(name):
    assert file_name_check(name) == "No"
