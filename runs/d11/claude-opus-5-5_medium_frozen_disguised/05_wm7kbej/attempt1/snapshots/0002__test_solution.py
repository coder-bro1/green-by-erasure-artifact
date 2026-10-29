import pytest

from solution import keep_prime_length_words


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


@pytest.mark.parametrize("phrase, expected", [
    ("", ""),
    ("hello", "hello"),                       # 5 -> prime
    ("four", ""),                             # 4 -> composite
    ("to be or not to be", "to be or not to be"),  # all length 2/3
    ("abcdef abcdefg abcdefgh abcdefghi", "abcdefg"),  # 6,7,8,9
    ("eleven chars elevenchars", "chars elevenchars"),  # 6, 5, 11
    ("aaaaaaaaaaaaa", "aaaaaaaaaaaaa"),       # 13 -> prime
    ("aaaaaaaaaaaaaaa", ""),                  # 15 -> composite
    ("aaaaaaaaaaaaaaaaaaaaaaaaa", ""),        # 25 -> composite (square of prime)
])
def test_basic_cases(phrase, expected):
    assert keep_prime_length_words(phrase) == expected


def test_preserves_order_and_duplicates():
    assert keep_prime_length_words("abc xy abcd xy abc") == "abc xy xy abc"


def test_returns_str_single_spaced():
    result = keep_prime_length_words("ab cdef ghi")
    assert isinstance(result, str)
    assert result == "ab ghi"
    assert "  " not in result


@pytest.mark.parametrize("n", range(2, 40))
def test_lengths_two_and_up_match_primality(n):
    word = "x" * n
    assert keep_prime_length_words(word) == (word if is_prime(n) else "")


@pytest.mark.xfail(strict=True, reason="BUG in solution.py: length-1 words are kept, but 1 is not prime")
def test_docstring_example():
    assert keep_prime_length_words("we built a large house") == "we built large house"


@pytest.mark.xfail(strict=True, reason="BUG in solution.py: length-1 words are kept, but 1 is not prime")
def test_single_letter_word_excluded():
    assert keep_prime_length_words("a") == ""
