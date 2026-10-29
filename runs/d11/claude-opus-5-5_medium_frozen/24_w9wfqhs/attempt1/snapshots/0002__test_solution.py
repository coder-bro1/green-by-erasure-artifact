import pytest

from solution import file_name_check


@pytest.mark.parametrize("name", [
    "example.txt",
    "a.exe",
    "Z.dll",
    "abc123.txt",       # exactly three digits
    "a1b2c3.dll",       # three digits spread out
    "MY16FILE3.exe",
    "a.txt",
    "K.dll",
])
def test_valid_names(name):
    assert file_name_check(name) == "Yes"


@pytest.mark.parametrize("name", [
    "1example.dll",     # starts with a digit
    "_example.txt",     # starts with underscore
    ".txt",             # empty name before dot
    "example",          # no dot
    "example.txt.txt",  # two dots
    "a..txt",           # two consecutive dots
    "abc1234.txt",      # four digits
    "a1b2c3d4.exe",     # four digits spread out
    "",                 # empty string
    "?aREYA.exe",
    " example.txt",     # leading space
    "1I563_Yes3.exe",
    "His12FILE94.exe",  # four digits
])
def test_invalid_names(name):
    assert file_name_check(name) == "No"


def test_returns_string():
    assert isinstance(file_name_check("example.txt"), str)
    assert isinstance(file_name_check("bad"), str)


# The docstring requires the extension to be one of ['txt', 'exe', 'dll'],
# but solution.py never checks the extension. These tests document the
# spec; strict xfail means they will start failing (alerting us) once fixed.
@pytest.mark.xfail(strict=True, reason="solution.py does not validate the extension")
@pytest.mark.parametrize("name", [
    "example.pdf",
    "example.",         # empty extension
    "example.TXT",      # case-sensitive per spec
    "example.txtx",
    "s.exe1",
])
def test_invalid_extension_spec(name):
    assert file_name_check(name) == "No"
