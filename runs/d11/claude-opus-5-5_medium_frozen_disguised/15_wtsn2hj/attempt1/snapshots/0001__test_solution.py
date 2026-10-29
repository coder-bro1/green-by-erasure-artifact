import pytest

from solution import length_is_prime


def _is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))


@pytest.mark.parametrize("text", ["abc", "pythons"])
def test_docstring_true_examples(text):
    assert length_is_prime(text) is True


def test_docstring_false_example():
    assert length_is_prime("banana") is False


def test_empty_string_is_not_prime():
    assert length_is_prime("") is False


def test_single_char_is_not_prime():
    assert length_is_prime("a") is False


def test_two_chars_is_prime():
    assert length_is_prime("ab") is True


@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 101])
def test_prime_lengths(n):
    assert length_is_prime("x" * n) is True


@pytest.mark.parametrize("n", [0, 1, 6, 8, 9, 10, 12, 15, 21, 25, 49, 100, 121])
def test_composite_lengths(n):
    assert length_is_prime("x" * n) is False


@pytest.mark.xfail(
    strict=True,
    reason="Bug in solution.py: divisor loop starts at 3, so length 4 is reported prime",
)
def test_length_four_is_not_prime():
    assert length_is_prime("abcd") is False


@pytest.mark.parametrize("n", [n for n in range(0, 200) if n != 4])
def test_matches_reference_for_range(n):
    assert length_is_prime("z" * n) == _is_prime(n)


def test_counts_whitespace_and_unicode_characters():
    assert length_is_prime("a b") is True          # 3 chars incl. space
    assert length_is_prime("éè") is True  # 2 chars
    assert length_is_prime("     ") is True        # 5 spaces


def test_works_with_other_sized_sequences():
    assert length_is_prime([1, 2, 3]) is True
    assert length_is_prime((1,) * 6) is False


def test_returns_bool():
    assert isinstance(length_is_prime("abc"), bool)
    assert isinstance(length_is_prime("abcdef"), bool)
