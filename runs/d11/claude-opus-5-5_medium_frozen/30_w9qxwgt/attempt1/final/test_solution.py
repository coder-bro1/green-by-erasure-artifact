import pytest

from solution import flip_case


@pytest.mark.parametrize(
    "inp, expected",
    [
        ("Hello", "hELLO"),  # docstring example
        ("", ""),
        ("hello", "HELLO"),
        ("HELLO", "hello"),
        ("Hello World!", "hELLO wORLD!"),
        ("These violent delights have violent ends",
         "tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS"),
        ("123 !@#", "123 !@#"),
        ("aBcDeF", "AbCdEf"),
    ],
)
def test_flip_case(inp, expected):
    assert flip_case(inp) == expected


def test_flip_twice_is_identity():
    s = "MiXeD CaSe 42"
    assert flip_case(flip_case(s)) == s


def test_returns_str():
    assert isinstance(flip_case("abc"), str)
