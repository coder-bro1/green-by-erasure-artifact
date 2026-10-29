import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "a.txt",
        "A.exe",
        "report.dll",
        "a123.txt",  # Three ASCII digits are allowed.
        "ab1c2d3.exe",
        "file name.txt",  # The rules do not restrict other characters in the name.
        "a١٢٣٤.txt",  # Non-ASCII numerals are not ASCII digits.
    ],
)
def test_names_that_meet_the_rules_are_accepted(file_name):
    assert file_name_check(file_name) == "Yes"


@pytest.mark.parametrize(
    "file_name",
    [
        "a1234.txt",  # More than three ASCII digits.
        "1example.dll",  # The first character must be a Latin letter.
        "éclair.txt",
        "Жfile.exe",
        ".txt",  # Empty name before the dot.
        "file",  # Missing dot and extension.
        "file.txt.exe",  # More than one dot.
        "file.pdf",  # Unsupported extension.
        "file.TXT",  # Extensions are case-sensitive.
        "file.txt.",  # Trailing extra dot.
    ],
)
def test_names_that_break_a_rule_are_rejected(file_name):
    assert file_name_check(file_name) == "No"
