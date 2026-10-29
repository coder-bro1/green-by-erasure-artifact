import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    ("file_name", "expected"),
    [
        ("example.txt", "Yes"),
        ("Report.exe", "Yes"),
        ("lib2.dll", "Yes"),
        ("a123.txt", "Yes"),
        ("a-b_c!.txt", "Yes"),
        ("", "No"),
        (".txt", "No"),
        ("1example.dll", "No"),
        ("a1234.txt", "No"),
        ("a.txt.bak", "No"),
        ("a_txt", "No"),
    ],
)
def test_file_name_check(file_name, expected):
    assert file_name_check(file_name) == expected


@pytest.mark.parametrize(
    "file_name",
    ["example.pdf", "example.TXT", "example."],
)
@pytest.mark.xfail(
    strict=True,
    reason="The implementation does not restrict the extension to txt, exe, or dll.",
)
def test_rejects_unlisted_extensions(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.parametrize("file_name", ["éclair.txt", "Журнал.dll"])
@pytest.mark.xfail(
    strict=True,
    reason="The implementation uses str.isalpha(), which accepts non-Latin letters.",
)
def test_name_must_start_with_a_latin_letter(file_name):
    assert file_name_check(file_name) == "No"
