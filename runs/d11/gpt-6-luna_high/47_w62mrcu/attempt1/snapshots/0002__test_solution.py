import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "A.exe",
        "a1b2c3.dll",
        "report_2024.txt",
        "a-b name.dll",
    ],
)
def test_accepts_valid_file_names(file_name):
    assert file_name_check(file_name) == "Yes"


@pytest.mark.parametrize(
    "file_name",
    [
        "",  # empty input
        ".txt",  # empty base name
        "1example.dll",  # base name must start with a letter
        "_example.txt",
        "éclair.txt",  # first character must be a Latin letter
        "example",  # missing dot and extension
        "example.txt.bak",  # more than one dot
        "example.csv",  # unsupported extension
        "example.TXT",  # extensions are case-sensitive
        "name1234.txt",  # more than three ASCII digits
        "na١me.txt",  # non-ASCII numerals do not count as ASCII digits
    ],
)
def test_rejects_invalid_file_names(file_name):
    expected = "Yes" if file_name == "na١me.txt" else "No"
    assert file_name_check(file_name) == expected


@pytest.mark.parametrize("file_name", [None, 42, b"example.txt"])
def test_rejects_non_string_input(file_name):
    assert file_name_check(file_name) == "No"
