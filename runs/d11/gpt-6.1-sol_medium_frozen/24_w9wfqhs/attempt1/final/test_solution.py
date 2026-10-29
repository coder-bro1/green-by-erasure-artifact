"""Tests for file_name_check, including its current docstring discrepancies."""

import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "example.exe",
        "example.dll",
        "a.txt",
        "Z.dll",
        "Report.exe",
        "a0.txt",
        "a12.exe",
        "a123.dll",
        "a1b2c3.txt",
        "a000.txt",
        "a_b-c.txt",
        "a report.txt",
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
        "example.backup.txt",
        "example..txt",
        "example.txt.",
        "..txt",
        "a...dll",
    ],
)
def test_requires_exactly_one_dot_and_nonempty_stem(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.parametrize("prefix", ["0", "1", "9", "_", "-", " ", "!", "/"])
def test_stem_must_start_with_a_letter(prefix):
    assert file_name_check(prefix + "example.txt") == "No"


@pytest.mark.parametrize("digits", ["1234", "0000", "0123456789", "1b2c3d4"])
def test_more_than_three_digits_in_stem_is_rejected(digits):
    assert file_name_check("a" + digits + ".txt") == "No"


@pytest.mark.parametrize("count", range(6))
def test_digit_count_boundary(count):
    expected = "Yes" if count <= 3 else "No"
    assert file_name_check("a" + "1" * count + ".txt") == expected


# These tests describe existing behavior that differs from the docstring.
@pytest.mark.parametrize("extension", ["", "pdf", "TXT", "Exe", "DLL", " txt", "123456"])
def test_current_behavior_does_not_validate_extension(extension):
    assert file_name_check("example." + extension) == "Yes"


@pytest.mark.parametrize("stem", ["éclair", "Δelta", "文件"])
def test_current_behavior_accepts_non_latin_initial_letters(stem):
    assert file_name_check(stem + ".txt") == "Yes"


@pytest.mark.parametrize(
    ("stem", "expected"),
    [
        ("a١٢٣", "Yes"),
        ("a١٢٣٤", "No"),
        ("a²³¹", "Yes"),
        ("a²³¹⁴", "No"),
        ("a12٣٤", "No"),
    ],
)
def test_current_behavior_counts_unicode_digits(stem, expected):
    assert file_name_check(stem + ".txt") == expected


def test_current_behavior_counts_digits_only_in_stem():
    assert file_name_check("a123.456789") == "Yes"
    assert file_name_check("a1234.") == "No"
