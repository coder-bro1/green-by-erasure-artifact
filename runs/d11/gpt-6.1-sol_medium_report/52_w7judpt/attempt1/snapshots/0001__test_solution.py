"""Tests for the filename validity rules documented in solution.py."""

import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "program.exe",
        "library.dll",
        "a.txt",
        "Z.exe",
        "a0.txt",
        "a12.dll",
        "a123.exe",
        "a1b2c3.txt",
        "a000.dll",
        "a-b_c.txt",
        "a b.txt",
        "a!@#.exe",
        "a\u00e9.txt",  # Only the first character must be a Latin letter.
        "a\u0661\u0662\u0663.txt",
    ],
)
def test_valid_file_names(file_name):
    assert file_name_check(file_name) == "Yes"


@pytest.mark.parametrize(
    "file_name",
    [
        "",
        "example",
        ".txt",
        ".",
        "example..txt",
        "example.part.txt",
        "example.txt.",
        ".example.txt",
        "1example.dll",
        "0.txt",
        "_example.txt",
        "-example.exe",
        " example.dll",
        "\nexample.txt",
        "a1234.txt",
        "a0000.exe",
        "a1b2c3d4.dll",
        "a1234567890.txt",
    ],
)
def test_invalid_structure_initial_character_or_digit_count(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.xfail(
    strict=True,
    reason="The implementation never checks that the extension is txt, exe, or dll.",
)
@pytest.mark.parametrize(
    "file_name",
    ["a.pdf", "a.csv", "a.", "a.TXT", "a.Exe", "a.DLL", "a.txt ", "a.txt\n", "a.1234"],
)
def test_invalid_extensions(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.xfail(
    strict=True,
    reason="str.isalpha() accepts non-Latin initials, contrary to the a-z/A-Z rule.",
)
@pytest.mark.parametrize("file_name", ["\u00e9.txt", "\u03b1.exe", "\u0416.dll", "\u4e2d.txt"])
def test_non_latin_initial_letters_are_invalid(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.xfail(
    strict=True,
    reason="str.isdigit() counts Unicode digits, but the docstring limits digits to 0-9.",
)
@pytest.mark.parametrize(
    "file_name",
    ["a\u0661\u0662\u0663\u0664.txt", "a\uff11\uff12\uff13\uff14.exe", "a123\u00b2.dll"],
)
def test_non_ascii_digits_do_not_count_toward_limit(file_name):
    assert file_name_check(file_name) == "Yes"
