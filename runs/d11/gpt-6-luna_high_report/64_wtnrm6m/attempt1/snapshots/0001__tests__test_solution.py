import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    ("file_name", "expected"),
    [
        ("example.txt", "Yes"),
        ("Report-2024.exe", "Yes"),
        ("a.dll", "Yes"),
        ("a123.txt", "Yes"),
        ("a1234.txt", "No"),
        ("1example.dll", "No"),
        (".txt", "No"),
        ("example", "No"),
        ("example.txt.exe", "No"),
        ("example.pdf", "No"),
        ("example.TXT", "No"),
        ("example.", "No"),
        ("example.tx t", "No"),
        ("a1b2c3.dll", "Yes"),
    ],
)
def test_file_name_check_documented_rules(file_name, expected):
    assert file_name_check(file_name) == expected


@pytest.mark.xfail(
    strict=True,
    reason="The implementation accepts Unicode letters, but the docstring permits only ASCII Latin letters.",
)
def test_initial_character_must_be_ascii_latin_letter():
    assert file_name_check("αlpha.txt") == "No"


@pytest.mark.xfail(
    strict=True,
    reason="The implementation counts all Unicode digits, but the docstring limits the count to ASCII 0-9.",
)
def test_only_ascii_digits_count_toward_digit_limit():
    assert file_name_check("a²³⁴⁵.txt") == "Yes"
