import pytest

from solution import file_name_check


@pytest.mark.parametrize("name", [
    "example.txt",
    "a.exe",
    "Z.dll",
    "abc123.txt",       # exactly three digits
    "a1b2c3.dll",
    "My_File-v2.exe",
    "a b.txt",
])
def test_valid_names(name):
    assert file_name_check(name) == "Yes"


@pytest.mark.parametrize("name", [
    "1example.dll",     # starts with a digit
    "_a.txt",           # starts with non-letter
    ".txt",             # empty prefix
    "",                 # empty string
    "example",          # no dot
    "a.b.txt",          # two dots
    "a..txt",
    "a.txt.",
    "a.pdf",            # bad extension
    "a.TXT",            # extension is case-sensitive
    "a.",               # empty extension
    "a.txt ",           # trailing space in extension
    "a1234.txt",        # four digits
    "a1b2c3d4.exe",
])
def test_invalid_names(name):
    assert file_name_check(name) == "No"


def test_returns_strings_exactly():
    assert file_name_check("example.txt") in ("Yes", "No")
    assert file_name_check("1example.dll") == "No"


def test_digits_in_extension_dont_matter_since_extension_is_fixed():
    assert file_name_check("abc12.txt") == "Yes"


@pytest.mark.xfail(strict=True, reason=(
    "Docstring requires the name to start with a latin letter ('a'-'z', 'A'-'Z'), "
    "but str.isalpha() also accepts non-latin letters such as 'é'."
))
@pytest.mark.parametrize("name", ["école.txt", "жfile.exe"])
def test_non_latin_first_letter_rejected(name):
    assert file_name_check(name) == "No"


@pytest.mark.xfail(strict=True, reason=(
    "Docstring counts only digits '0'-'9'; str.isdigit() also counts Unicode "
    "digits such as superscripts, so 'a123².txt' (three ASCII digits) is rejected."
))
def test_only_ascii_digits_counted():
    assert file_name_check("a123².txt") == "Yes"
