import pytest

from solution import file_name_check


@pytest.mark.parametrize(
    "file_name",
    [
        "example.txt",
        "program.exe",
        "library.dll",
        "a.txt",
        "Z.dll",
        "a0.txt",
        "a12.exe",
        "a123.dll",
        "a1b2c3.txt",
        "Report_202.txt",
        "a-b c!.exe",
        "aé.txt",
        "a١٢٣٤.txt",
        "a²³⁴⁵.dll",
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
        ".txt",
        ".",
        "example.",
        "example..txt",
        "example.backup.txt",
        "example.txt.",
        "1example.dll",
        "_example.txt",
        "-example.exe",
        " example.txt",
        "éxample.txt",
        "Ωmega.dll",
        "文件.exe",
        "a1234.txt",
        "a1b2c3d4.dll",
        "example.csv",
        "example.TXT",
        "example.Exe",
        "example.DLL",
        "example.txt ",
        "example. txt",
        "example.txt\n",
        "example.txt1",
    ],
)
def test_invalid_file_names(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.parametrize("initial", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
def test_every_latin_letter_can_start_a_file_name(initial):
    assert file_name_check(f"{initial}.txt") == "Yes"
