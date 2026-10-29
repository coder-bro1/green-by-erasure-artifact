"""Tests for validate_filename, including its current undocumented behavior."""

import pytest

from solution import validate_filename


@pytest.mark.parametrize(
    "name",
    [
        "report7.exe",
        "a.txt",
        "Z.exe",
        "library.dll",
        "REPORT.TXT",  # Extension case is not checked by the implementation.
        "a0.txt",
        "a12.exe",
        "a123.dll",
        "a1b2c3.txt",
        "Report_202.dll",
        "a-b.txt",
        "a b.exe",
        "a!.dll",
    ],
)
def test_valid_names(name):
    assert validate_filename(name) == "Yes"


@pytest.mark.parametrize(
    "name",
    [
        "",
        "report",
        "reporttxt",
        ".",
        ".txt",
        "report..txt",
        "report.txt.exe",
        ".report.txt",
        "report.txt.",
        "7report.exe",
        "123.txt",
        "_report.txt",
        "-report.exe",
        " report.dll",
        "!report.txt",
        "x1234.txt",
        "a1b2c3d4.exe",
        "report0123456789.dll",
    ],
)
def test_invalid_names(name):
    assert validate_filename(name) == "No"


@pytest.mark.parametrize("extension", ["", "pdf", "TXT", "Exe", "123456", "tar", " "])
def test_current_behavior_accepts_unrestricted_extensions(extension):
    """The docstring restricts extensions, but the code never checks them."""
    assert validate_filename(f"report.{extension}") == "Yes"


@pytest.mark.parametrize("name", ["é.txt", "Ω.exe", "中.dll"])
def test_current_behavior_accepts_non_latin_initial_letters(name):
    """str.isalpha accepts letters beyond the docstring's a-z and A-Z."""
    assert validate_filename(name) == "Yes"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("a١٢٣.txt", "Yes"),
        ("a١٢٣٤.txt", "No"),
        ("a²³⁴.txt", "Yes"),
        ("a²³⁴⁵.txt", "No"),
        ("a123.4567", "Yes"),
        ("a1234.exe", "No"),
    ],
)
def test_digit_count_uses_isdigit_on_stem_only(name, expected):
    assert validate_filename(name) == expected
