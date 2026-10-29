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
        "Report.txt",
        "a1.exe",
        "a12.dll",
        "a123.txt",
        "a1b2c3.exe",
        "a000.dll",
        "a_name-with spaces!.txt",
        "aé.txt",
        "a²٣４.txt",
        "a²٣４5.txt",
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
        "example.",
        ".",
        "example.tar.txt",
        "example..txt",
        "example.txt.",
        "example.csv",
        "example.TXT",
        "example.Exe",
        "example.DLL",
        "example.txt ",
        "example. txt",
        "1example.dll",
        "_example.txt",
        "-example.exe",
        " example.txt",
        "éxample.txt",
        "中.txt",
        "a1234.txt",
        "a1b2c3d4.exe",
        "a0000.dll",
    ],
)
def test_invalid_file_names(file_name):
    assert file_name_check(file_name) == "No"


@pytest.mark.parametrize("first_letter", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
@pytest.mark.parametrize("extension", ["txt", "exe", "dll"])
def test_all_latin_initial_letters_and_allowed_extensions(first_letter, extension):
    assert file_name_check(f"{first_letter}.{extension}") == "Yes"


@pytest.mark.parametrize("digit", "0123456789")
def test_ascii_digit_limit(digit):
    assert file_name_check(f"a{digit * 3}.txt") == "Yes"
    assert file_name_check(f"a{digit * 4}.txt") == "No"
