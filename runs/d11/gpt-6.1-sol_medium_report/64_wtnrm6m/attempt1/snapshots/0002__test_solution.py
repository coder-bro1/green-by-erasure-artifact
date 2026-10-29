import string

import pytest

from solution import file_name_check


@pytest.mark.parametrize("extension", ["txt", "exe", "dll"])
@pytest.mark.parametrize("first_letter", list(string.ascii_letters))
def test_all_latin_initial_letters_and_supported_extensions(first_letter, extension):
    assert file_name_check(f"{first_letter}example.{extension}") == "Yes"


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "a.exe",
        "Z.dll",
        "a0.txt",
        "a12.exe",
        "a123.dll",
        "a1b2c3.txt",
        "a000.txt",
        "a_-.txt",
        "a b.txt",
        "a\u00e9.txt",
        "a\u4e2d.txt",
    ],
)
def test_valid_file_names(file_name):
    assert file_name_check(file_name) == "Yes"


@pytest.mark.parametrize(
    "file_name",
    [
        "",
        "example",
        "exampletxt",
        ".",
        ".txt",
        "example.",
        "example..txt",
        "example.backup.txt",
        "example.txt.",
        "1example.dll",
        "0.txt",
        "_example.txt",
        "-example.txt",
        " example.txt",
        "example.pdf",
        "example.TXT",
        "example.Exe",
        "example.DLL",
        "example.txt ",
        "example. txt",
        "a1234.txt",
        "a0000.exe",
        "a1b2c3d4.dll",
        "a0123456789.txt",
    ],
)
def test_invalid_file_names(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.xfail(
    strict=True,
    reason="isalpha() accepts non-ASCII initial letters, but the docstring requires a-z or A-Z",
)
@pytest.mark.parametrize("first_character", ["\u00e9", "\u03a9", "\u4e2d"])
def test_initial_letter_must_be_ascii_latin(first_character):
    assert file_name_check(f"{first_character}example.txt") == "No"


@pytest.mark.xfail(
    strict=True,
    reason="isdigit() counts Unicode digits, but the docstring limits the count to 0-9",
)
@pytest.mark.parametrize(
    "file_name",
    ["a\u0661\u0662\u0663\u0664.txt", "a\uff11\uff12\uff13\uff14.exe", "a123\u00b2.dll"],
)
def test_only_ascii_digits_count_toward_digit_limit(file_name):
    assert file_name_check(file_name) == "Yes"
