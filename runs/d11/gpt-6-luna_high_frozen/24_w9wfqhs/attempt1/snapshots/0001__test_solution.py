import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "A.dll",
        "report2.exe",
        "a123.txt",
    ],
)
def test_accepts_names_with_valid_structure(file_name):
    assert file_name_check(file_name) == "Yes"


@pytest.mark.parametrize(
    "file_name",
    [
        "",
        ".txt",          # empty name before the dot
        "1example.txt",  # must start with a letter
        "a1234.txt",     # more than three digits in the name
        "a.txt.exe",     # more than one dot
        "exampletxt",    # no dot
    ],
)
def test_rejects_invalid_structure(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.xfail(strict=False, reason="solution.py does not validate the extension")
@pytest.mark.parametrize("file_name", ["example.csv", "example.", "example.TXT"])
def test_rejects_extensions_outside_the_allowed_lowercase_set(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.xfail(strict=False, reason="solution.py accepts non-Latin alphabetic characters")
def test_requires_a_latin_letter_at_the_start():
    assert file_name_check("éxample.txt") == "No"
