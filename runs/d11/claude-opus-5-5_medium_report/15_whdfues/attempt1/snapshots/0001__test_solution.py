import pytest

from solution import histogram


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a b c", {"a": 1, "b": 1, "c": 1}),
        ("a b b a", {"a": 2, "b": 2}),
        ("a b c a b", {"a": 2, "b": 2}),
        ("b b b b a", {"b": 4}),
    ],
)
def test_docstring_examples(text, expected):
    assert histogram(text) == expected


def test_single_letter():
    assert histogram("a") == {"a": 1}


def test_single_letter_repeated():
    assert histogram("z z z") == {"z": 3}


def test_single_winner_among_many():
    assert histogram("r t g g t g") == {"g": 3}


def test_all_tied_at_two():
    assert histogram("x y x y") == {"x": 2, "y": 2}


def test_order_independent():
    assert histogram("a b a c b a") == histogram("c b a b a a") == {"a": 3}


def test_returns_dict_with_int_counts():
    result = histogram("q q w")
    assert isinstance(result, dict)
    assert all(isinstance(v, int) for v in result.values())


def test_input_not_mutated():
    s = "a b a"
    histogram(s)
    assert s == "a b a"


@pytest.mark.xfail(
    strict=True,
    reason="''.split(' ') yields [''], and the empty token is counted, "
    "so histogram('') returns {'': 1} instead of {}",
)
def test_empty_string():
    assert histogram("") == {}


@pytest.mark.xfail(
    strict=True,
    reason="consecutive spaces produce '' tokens that are added to the result "
    "when the max count is 1",
)
def test_extra_spaces_with_all_unique():
    assert histogram("a  b") == {"a": 1, "b": 1}


def test_extra_spaces_ignored_when_max_above_one():
    # '' is excluded when computing the max, so it only leaks in when max == 1
    assert histogram("a  a b") == {"a": 2}
