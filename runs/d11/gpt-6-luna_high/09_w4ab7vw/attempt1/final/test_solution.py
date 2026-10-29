import pytest

from solution import prime_length


@pytest.mark.parametrize("value", ["", "a"])
def test_lengths_zero_and_one_are_not_prime(value):
    assert prime_length(value) is False


@pytest.mark.parametrize("value", ["ab", "abc", "abcde", "abcdefg", "abcdefghijk"])
def test_prime_lengths_return_true(value):
    assert prime_length(value) is True


@pytest.mark.parametrize("value", ["abcd", "abcdef", "abcdefgh", "abcdefghij", "abcdefghijkl"])
def test_composite_lengths_return_false(value):
    assert prime_length(value) is False


def test_non_ascii_characters_are_counted_as_characters():
    assert prime_length("ééé") is True
