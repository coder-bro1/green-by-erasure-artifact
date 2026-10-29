from solution import flip_case


def test_flips_lowercase_to_uppercase():
    assert flip_case("hello") == "HELLO"


def test_flips_uppercase_to_lowercase():
    assert flip_case("HELLO") == "hello"


def test_flips_each_letter_in_mixed_case_text():
    assert flip_case("Hello, World!") == "hELLO, wORLD!"


def test_leaves_nonletters_unchanged():
    assert flip_case("123 !? -_=+") == "123 !? -_=+"


def test_empty_string_returns_empty_string():
    assert flip_case("") == ""


def test_flips_unicode_letters():
    assert flip_case("\u00c4\u00df") == "\u00e4SS"
