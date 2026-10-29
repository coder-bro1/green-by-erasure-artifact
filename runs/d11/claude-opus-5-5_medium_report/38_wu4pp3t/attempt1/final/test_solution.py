import pytest

from solution import flip_case

BUG = "flip_case returns string.lower() instead of swapping case; lowercase letters are never uppercased"


def test_empty_string():
    assert flip_case("") == ""


def test_all_uppercase_becomes_lowercase():
    assert flip_case("ABC") == "abc"


def test_non_letters_unchanged():
    assert flip_case("123 !?.-_\n") == "123 !?.-_\n"


def test_returns_str():
    assert isinstance(flip_case("ABC"), str)


@pytest.mark.xfail(strict=True, reason=BUG)
def test_docstring_example():
    assert flip_case("Hello") == "hELLO"


@pytest.mark.xfail(strict=True, reason=BUG)
def test_all_lowercase_becomes_uppercase():
    assert flip_case("abc") == "ABC"


@pytest.mark.xfail(strict=True, reason=BUG)
def test_mixed_case_with_punctuation():
    assert flip_case("These violent delights have violent ends") == "tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS"


@pytest.mark.xfail(strict=True, reason=BUG)
def test_mixed_with_digits():
    assert flip_case("aB1cD2") == "Ab1Cd2"


@pytest.mark.xfail(strict=True, reason=BUG)
def test_flip_twice_is_identity():
    s = "Hello World 42"
    assert flip_case(flip_case(s)) == s
