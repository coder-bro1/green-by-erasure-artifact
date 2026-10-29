import pytest

from solution import is_happy

BUG_REASON = (
    "Known bug in solution.py: it only rejects windows where all three chars are "
    "equal, instead of any two being equal (spec: every 3 consecutive letters distinct)."
)


# --- Length < 3 is never happy ---
@pytest.mark.parametrize("s", ["", "a", "aa", "ab"])
def test_too_short(s):
    assert is_happy(s) is False


# --- Cases where every 3-window is fully distinct -> happy ---
@pytest.mark.parametrize("s", ["abc", "adb", "abcd", "abcabc", "xyzxyz", "iopaxpoi", "123", "a b"])
def test_happy_strings(s):
    assert is_happy(s) is True


# --- All three equal in some window -> unhappy (implementation handles this) ---
@pytest.mark.parametrize("s", ["aaa", "aaaa", "abccc", "zzzab", "abcddd"])
def test_triple_repeat_is_unhappy(s):
    assert is_happy(s) is False


# --- Two-of-three equal in a window -> unhappy per spec, but buggy implementation says True ---
@pytest.mark.xfail(strict=True, reason=BUG_REASON)
@pytest.mark.parametrize("s", ["aabb", "xyy", "aba", "abb", "aab", "iopaxioi", "abcdcx"])
def test_pair_repeat_is_unhappy_per_spec(s):
    assert is_happy(s) is False


# --- Pins the current (buggy) behaviour so any change is noticed ---
@pytest.mark.parametrize("s", ["aabb", "xyy", "aba"])
def test_current_behaviour_pair_repeat_returns_true(s):
    assert is_happy(s) is True


def test_returns_bool():
    assert isinstance(is_happy("abc"), bool)
    assert isinstance(is_happy("a"), bool)
    assert isinstance(is_happy("aaa"), bool)
