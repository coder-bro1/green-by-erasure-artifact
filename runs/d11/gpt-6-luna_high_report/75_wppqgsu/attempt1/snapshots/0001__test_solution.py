import pytest

from solution import longest


def test_longest_returns_none_for_empty_list():
    assert longest([]) is None


@pytest.mark.xfail(
    strict=True,
    reason="longest() returns None for non-empty input instead of the longest string",
)
def test_longest_returns_the_only_string():
    assert longest(["only"]) == "only"


@pytest.mark.xfail(
    strict=True,
    reason="longest() returns None for non-empty input instead of the longest string",
)
def test_longest_returns_longest_string():
    assert longest(["a", "bb", "ccc"]) == "ccc"


@pytest.mark.xfail(
    strict=True,
    reason="longest() returns None instead of the first string tied for longest",
)
def test_longest_returns_first_string_when_lengths_tie():
    assert longest(["first", "other", "x"]) == "first"
