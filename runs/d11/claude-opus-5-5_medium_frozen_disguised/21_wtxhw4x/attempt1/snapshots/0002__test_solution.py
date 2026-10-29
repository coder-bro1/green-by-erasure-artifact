import multiprocessing

import pytest

from solution import reads_same, shortest_mirror_extension

TIMEOUT_SECONDS = 2


def _worker(text, queue):
    queue.put(shortest_mirror_extension(text))


def run_with_timeout(text):
    """Run shortest_mirror_extension in a child process so a hang fails the test instead of freezing pytest."""
    queue = multiprocessing.Queue()
    proc = multiprocessing.Process(target=_worker, args=(text, queue))
    proc.start()
    proc.join(TIMEOUT_SECONDS)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        pytest.fail(f"shortest_mirror_extension({text!r}) did not finish within {TIMEOUT_SECONDS}s")
    return queue.get(timeout=1)


def brute_force(text):
    for cut in range(len(text) + 1):
        if reads_same(text[cut:]):
            return text + text[:cut][::-1]


# --- reads_same ---

@pytest.mark.parametrize("text", ["", "a", "aa", "aba", "abba", "racecar", "abcba"])
def test_reads_same_true(text):
    assert reads_same(text) is True


@pytest.mark.parametrize("text", ["ab", "abc", "abca", "Aa", "ab a"])
def test_reads_same_false(text):
    assert reads_same(text) is False


# --- shortest_mirror_extension: inputs that are already palindromes ---

@pytest.mark.parametrize("text", ["", "a", "aa", "aba", "abba", "racecar"])
def test_palindrome_input_unchanged(text):
    assert run_with_timeout(text) == text


# --- shortest_mirror_extension: inputs that need characters appended ---

@pytest.mark.parametrize(
    "text, expected",
    [
        ("abc", "abcba"),      # docstring example
        ("abcb", "abcba"),     # docstring example
        ("ab", "aba"),
        ("aab", "aabaa"),
        ("abcd", "abcdcba"),
        ("aacecaaa", "aacecaaacecaa"),
        ("abab", "ababa"),
    ],
)
def test_appends_minimal_suffix(text, expected):
    assert run_with_timeout(text) == expected


@pytest.mark.parametrize("text", ["xyz", "banana", "abcdefg", "aabba", "noonx"])
def test_properties(text):
    result = run_with_timeout(text)
    assert result.startswith(text)
    assert reads_same(result)
    assert result == brute_force(text)
    assert len(result) <= 2 * len(text) - 1
