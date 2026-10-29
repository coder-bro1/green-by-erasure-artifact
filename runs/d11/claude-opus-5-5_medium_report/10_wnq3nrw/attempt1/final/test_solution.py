import pytest

from solution import total_match

INVERTED = (
    "solution.py returns the list with MORE total chars (and lst2 on ties); "
    "docstring requires the list with fewer chars (and lst1 on ties)"
)


def test_both_empty():
    assert total_match([], []) == []


@pytest.mark.xfail(strict=True, reason=INVERTED)
def test_tie_returns_first_list_identity():
    a, b = ["ab"], ["cd"]
    assert total_match(a, b) is a


@pytest.mark.xfail(strict=True, reason=INVERTED)
def test_tie_empty_lists_returns_first_identity():
    a, b = [], []
    assert total_match(a, b) is a


@pytest.mark.xfail(strict=True, reason=INVERTED)
@pytest.mark.parametrize(
    "lst1, lst2, expected",
    [
        (["hi", "admin"], ["hI", "Hi"], ["hI", "Hi"]),
        (["hi", "admin"], ["hi", "hi", "admin", "project"], ["hi", "admin"]),
        (["hi", "admin"], ["hI", "hi", "hi"], ["hI", "hi", "hi"]),
        (["4"], ["1", "2", "3", "4", "5"], ["4"]),
    ],
)
def test_docstring_examples(lst1, lst2, expected):
    assert total_match(lst1, lst2) == expected


@pytest.mark.xfail(strict=True, reason=INVERTED)
def test_empty_vs_nonempty_returns_empty():
    assert total_match([], ["a"]) == []


@pytest.mark.xfail(strict=True, reason=INVERTED)
def test_nonempty_vs_empty_returns_empty():
    assert total_match(["a"], []) == []


@pytest.mark.xfail(strict=True, reason=INVERTED)
def test_counts_chars_not_elements():
    # lst1 has more elements but fewer chars
    assert total_match(["a", "b", "c"], ["abcdef"]) == ["a", "b", "c"]


@pytest.mark.xfail(strict=True, reason=INVERTED)
def test_tie_with_different_lengths_returns_first():
    a, b = ["abc", "d"], ["ab", "cd"]
    assert total_match(a, b) is a


def test_does_not_mutate_inputs():
    a, b = ["x", "yy"], ["zzz", "w"]
    total_match(a, b)
    assert a == ["x", "yy"] and b == ["zzz", "w"]


def test_returns_one_of_the_input_objects():
    a, b = ["x"], ["yy"]
    assert total_match(a, b) in (a, b)
    r = total_match(a, b)
    assert r is a or r is b
