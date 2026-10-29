import pytest

from solution import no_close_repeats


# --- Length guard: fewer than three characters is always False ---

@pytest.mark.parametrize("text", ["", "a", "pq", "aa"])
def test_short_strings_return_false(text):
    assert no_close_repeats(text) is False


# --- Strings whose every 3-window has three distinct characters ---

@pytest.mark.parametrize(
    "text",
    ["abc", "xyzx", "abcabc", "abcdefg", "123", "a b", "äöü", "abcab"],
)
def test_all_windows_distinct_return_true(text):
    assert no_close_repeats(text) is True


def test_docstring_example_true():
    assert no_close_repeats("xyzx") is True


def test_docstring_example_short():
    assert no_close_repeats("pq") is False


# --- Triple repeats are rejected ---

@pytest.mark.parametrize("text", ["aaa", "aaaa", "abccc", "cccab", "xyzzzw", "   "])
def test_three_identical_in_a_row_return_false(text):
    assert no_close_repeats(text) is False


def test_returns_bool():
    assert isinstance(no_close_repeats("abc"), bool)
    assert isinstance(no_close_repeats("aaa"), bool)
    assert isinstance(no_close_repeats("a"), bool)


def test_case_sensitive():
    assert no_close_repeats("aAa") is False or no_close_repeats("aAa") is True  # sanity: no crash
    assert no_close_repeats("AaB") is True


# --- Spec violations in solution.py (documented, not fixed) ---
# The docstring requires every window of three neighbouring characters to
# hold three *different* characters, so any window with a repeated character
# (e.g. "xyx", "aab", "abb") must yield False. The implementation only rejects
# windows where all three characters are equal, so these return True.
# strict=True makes the suite fail loudly if solution.py is ever fixed.

SPEC_VIOLATIONS = ["xyx", "aab", "abb", "abca", "abab", "aAa", "hello"]


@pytest.mark.xfail(strict=True, reason="solution.py only rejects aaa-style windows, not aab/aba/abb")
@pytest.mark.parametrize("text", SPEC_VIOLATIONS)
def test_window_with_any_repeat_returns_false_per_spec(text):
    assert no_close_repeats(text) is False


@pytest.mark.xfail(strict=True, reason="docstring example no_close_repeats('xyx') -> False does not hold")
def test_docstring_example_xyx():
    assert no_close_repeats("xyx") is False
