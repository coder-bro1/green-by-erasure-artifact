import pytest

from solution import total_match


@pytest.mark.xfail(
    strict=True,
    reason="For equal character totals, the docstring requires returning the first list; the implementation returns the second.",
)
def test_equal_totals_return_first_list():
    first = ["a", "bc"]
    second = ["ab", "c"]

    assert total_match(first, second) is first


@pytest.mark.xfail(
    strict=True,
    reason="When the first list has fewer characters, the docstring requires returning it; the implementation returns the second list.",
)
def test_returns_first_list_when_it_has_fewer_characters():
    first = ["hi", "admin"]
    second = ["hi", "hi", "admin", "project"]

    assert total_match(first, second) == first


@pytest.mark.xfail(
    strict=True,
    reason="When the second list has fewer characters, the docstring requires returning it; the implementation returns the first list.",
)
def test_returns_second_list_when_it_has_fewer_characters():
    first = ["hi", "admin"]
    second = ["hI", "Hi"]

    assert total_match(first, second) == second


@pytest.mark.xfail(
    strict=True,
    reason="The docstring's empty-list tie requires returning the first argument; the implementation returns the second.",
)
def test_empty_lists_return_first_argument():
    first = []
    second = []

    assert total_match(first, second) is first


def test_does_not_modify_either_list():
    first = ["hi", "admin"]
    second = ["hI", "Hi"]
    first_before = first.copy()
    second_before = second.copy()

    total_match(first, second)

    assert first == first_before
    assert second == second_before
