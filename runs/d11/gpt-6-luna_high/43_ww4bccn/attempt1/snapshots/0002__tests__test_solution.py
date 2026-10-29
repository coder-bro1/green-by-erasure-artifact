from solution import longest


def test_longest_returns_none_for_empty_list():
    assert longest([]) is None


def test_longest_returns_the_only_string():
    assert longest(["only"]) == "only"


def test_longest_returns_string_with_greatest_length():
    assert longest(["a", "longest", "mid"]) == "longest"


def test_longest_returns_first_string_when_lengths_tie():
    assert longest(["first", "other", "last"]) == "first"


def test_longest_returns_first_of_multiple_longest_strings():
    assert longest(["short", "winner", "also wins", "winner"]) == "also wins"
