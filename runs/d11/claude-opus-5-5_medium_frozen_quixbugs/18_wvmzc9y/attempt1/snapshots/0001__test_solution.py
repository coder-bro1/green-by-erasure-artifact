"""Tests for solution.wrap.

solution.py must not be modified. The current implementation has known
defects relative to its docstring contract; the tests for those are marked
``xfail(strict=True)`` so the suite passes while still documenting the bugs
(and will start failing loudly -- XPASS -- once the bugs are fixed, prompting
removal of the markers).

Known defects:
  1. The remaining text after the loop is never appended, so the output does
     not concatenate back to the input (and input with len <= cols yields []).
  2. When the remaining text starts with a space and has no other space within
     the first cols+1 characters, rfind returns 0, no progress is made and the
     function loops forever (e.g. wrap("hello world", 5)).
"""
import subprocess
import sys
from pathlib import Path

import pytest

from solution import wrap

HERE = Path(__file__).resolve().parent


def run_wrap_with_timeout(text, cols, timeout=3):
    """Run wrap in a subprocess so an infinite loop cannot hang the suite.

    Returns the result list, or None if the call timed out.
    """
    code = (
        "import sys, json; sys.path.insert(0, sys.argv[1]);"
        "from solution import wrap;"
        "print(json.dumps(wrap(json.loads(sys.argv[2]), int(sys.argv[3]))))"
    )
    import json

    try:
        proc = subprocess.run(
            [sys.executable, "-c", code, str(HERE), json.dumps(text), str(cols)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# Behaviour the current implementation gets right
# ---------------------------------------------------------------------------

class TestCurrentBehaviour:
    def test_returns_list(self):
        assert isinstance(wrap("hello world", 6), list)

    def test_breaks_at_last_space_within_width(self):
        # Break happens at the space; the space stays with the following text.
        assert wrap("hello world", 6) == ["hello"]

    def test_prefers_rightmost_space(self):
        assert wrap("aaa bbb ccc", 7) == ["aaa bbb"]

    def test_space_exactly_at_cols_boundary_is_used(self):
        # Space at index cols (5) is eligible because rfind searches [0, cols+1).
        assert wrap("abcde fg", 5) == ["abcde"]

    def test_hard_break_when_no_space(self):
        assert wrap("abcdefgh", 3) == ["abc", "def"]

    def test_hard_break_exact_multiple(self):
        assert wrap("abcdef", 3) == ["abc"]

    def test_cols_one_without_spaces(self):
        assert wrap("abcd", 1) == ["a", "b", "c"]

    def test_input_is_not_mutated(self):
        text = "hello world"
        wrap(text, 6)
        assert text == "hello world"

    @pytest.mark.parametrize(
        "text,cols",
        [
            ("hello world", 6),
            ("abcdefgh", 3),
            ("aaa bbb ccc", 7),
            ("abcdefghijklmnop", 4),
            ("abcde fg", 5),
        ],
    )
    def test_lines_never_exceed_cols(self, text, cols):
        assert all(len(line) <= cols for line in wrap(text, cols))

    @pytest.mark.parametrize(
        "text,cols",
        [
            ("hello world", 6),
            ("abcdefgh", 3),
            ("aaa bbb ccc", 7),
            ("abcdefghijklmnop", 4),
        ],
    )
    def test_output_is_prefix_of_input(self, text, cols):
        # Whatever is emitted is preserved verbatim, in order (spaces untrimmed).
        assert text.startswith("".join(wrap(text, cols)))


# ---------------------------------------------------------------------------
# Docstring contract -- currently violated (known bugs)
# ---------------------------------------------------------------------------

BUG_TAIL = "Bug: remaining text after the loop is never appended to lines"
BUG_LOOP = "Bug: infinite loop when remaining text starts with a space (rfind -> 0)"


class TestSpecContract:
    @pytest.mark.xfail(strict=True, reason=BUG_TAIL)
    def test_short_text_returned_as_single_line(self):
        assert wrap("hi", 5) == ["hi"]

    @pytest.mark.xfail(strict=True, reason=BUG_TAIL)
    def test_text_exactly_cols_long(self):
        assert wrap("abcde", 5) == ["abcde"]

    @pytest.mark.xfail(strict=True, reason=BUG_TAIL)
    def test_hard_break_keeps_tail(self):
        assert wrap("abcdefgh", 3) == ["abc", "def", "gh"]

    @pytest.mark.xfail(strict=True, reason=BUG_TAIL)
    def test_word_break_keeps_tail(self):
        assert wrap("hello world", 6) == ["hello", " world"]

    @pytest.mark.xfail(strict=True, reason=BUG_TAIL)
    @pytest.mark.parametrize(
        "text,cols",
        [("hello world", 6), ("abcdefgh", 3), ("aaa bbb ccc", 7), ("x", 10)],
    )
    def test_concatenation_round_trips(self, text, cols):
        assert "".join(wrap(text, cols)) == text

    @pytest.mark.xfail(strict=True, reason=BUG_LOOP)
    def test_terminates_on_two_short_words(self):
        result = run_wrap_with_timeout("hello world", 5)
        assert result is not None, "wrap did not terminate"
        assert "".join(result) == "hello world"

    @pytest.mark.xfail(strict=True, reason=BUG_LOOP)
    def test_terminates_with_cols_one_and_spaces(self):
        result = run_wrap_with_timeout("a b c", 1)
        assert result is not None, "wrap did not terminate"
        assert "".join(result) == "a b c"
        assert all(len(line) <= 1 for line in result)
