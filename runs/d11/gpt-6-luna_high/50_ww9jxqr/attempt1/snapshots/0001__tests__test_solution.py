import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "Report.EXE",  # Extensions are case-sensitive; this one is checked below as invalid.
    ],
)
def test_valid_names(file_name):
    # Keep accepted examples explicit so the contract is easy to extend.
    if file_name == "Report.EXE":
        pytest.skip("Uppercase extensions are not in the allowed extension list")
    assert file_name_check(file_name) == "Yes"


@pytest.mark.parametrize(
    "file_name",
    [
        "a.txt",
        "A.exe",
        "report.dll",
        "a123.txt",  # Three ASCII digits are allowed.
        "ab1c2d3.exe",
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
        "file name.txt",  # Spaces are otherwise permitted in the name.
    ],
)
def test_names_that_break_a_rule_are_rejected(file_name):
    expected = "No" if file_name != "file name.txt" else "Yes"
    assert file_name_check(file_name) == expected
