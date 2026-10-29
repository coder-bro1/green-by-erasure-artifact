import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "A.exe",
        "a1b2c3.dll",
        "report_204.txt",
        "a-b name.dll",
        "na١me.txt",  # only ASCII digits count toward the limit
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
    ],
)
def test_rejects_invalid_file_names(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.parametrize("file_name", [None, 42, b"example.txt"])
def test_rejects_non_string_input(file_name):
    assert file_name_check(file_name) == "No"
