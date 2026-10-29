import pytest

from solution import flip_case


def test_docstring_example():
    assert flip_case('Hello') == 'hELLO'


def test_empty_string():
    assert flip_case('') == ''


@pytest.mark.parametrize(
    "inp, expected",
    [
        ('abc', 'ABC'),
        ('ABC', 'abc'),
        ('aBcDeF', 'AbCdEf'),
        ('Hello World', 'hELLO wORLD'),
        ('These violent delights have violent ends',
         'tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS'),
    ],
)
def test_letters(inp, expected):
    assert flip_case(inp) == expected


@pytest.mark.parametrize("inp", ['12345', '   ', '!@#$%^&*()', '\n\t', '-_=+'])
def test_non_letters_unchanged(inp):
    assert flip_case(inp) == inp


def test_mixed_letters_and_symbols():
    assert flip_case('Hello, World! 123') == 'hELLO, wORLD! 123'


def test_non_ascii_letters():
    assert flip_case('Ärger über Éclair') == 'äRGER ÜBER éCLAIR'


@pytest.mark.parametrize("s", ['', 'Hello', 'aBc 123 XyZ!', 'Éclair'])
def test_involution(s):
    assert flip_case(flip_case(s)) == s


def test_returns_str_and_preserves_length():
    s = 'MiXeD CaSe'
    result = flip_case(s)
    assert isinstance(result, str)
    assert len(result) == len(s)


def test_input_not_mutated():
    s = 'Hello'
    flip_case(s)
    assert s == 'Hello'
