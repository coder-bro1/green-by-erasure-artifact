import pytest

from solution import invert_letter_case


@pytest.mark.parametrize(
    "text, expected",
    [
        ("PyThon 3", "pYtHON 3"),  # docstring example
        ("", ""),
        ("abc", "ABC"),
        ("ABC", "abc"),
        ("Hello, World!", "hELLO, wORLD!"),
        ("123 !@#", "123 !@#"),
        ("a", "A"),
        ("Z", "z"),
        ("MiXeD cAsE", "mIxEd CaSe"),
    ],
)
def test_invert_letter_case(text, expected):
    assert invert_letter_case(text) == expected


def test_non_letters_unchanged():
    text = "0123456789 \t\n-_=+[]{};:'\",.<>/?"
    assert invert_letter_case(text) == text


def test_double_inversion_is_identity():
    text = "The Quick Brown Fox 42"
    assert invert_letter_case(invert_letter_case(text)) == text


def test_returns_str():
    assert isinstance(invert_letter_case("abc"), str)
