import pytest

from solution import select_words


@pytest.mark.parametrize(
    ("text", "count", "expected"),
    [
        ("Mary had a little lamb", 4, ["little"]),
        ("Mary had a little lamb", 3, ["Mary", "lamb"]),
        ("simple white space", 2, []),
        ("Hello world", 4, ["world"]),
        ("Uncle sam", 3, ["Uncle"]),
    ],
)
def test_documented_examples(text, count, expected):
    assert select_words(text, count) == expected


@pytest.mark.parametrize("text", ["", " ", "     "])
@pytest.mark.parametrize("count", [0, 1, 4])
def test_empty_or_space_only_input(text, count):
    assert select_words(text, count) == []


@pytest.mark.parametrize(
    ("text", "count", "expected"),
    [
        ("a E i O u AEIOU", 0, ["a", "E", "i", "O", "u", "AEIOU"]),
        ("a E i O u AEIOU", 1, []),
        ("b BC bCd AEIOU", 3, ["bCd"]),
        ("Hello HELLO hElLo world WORLD", 3, ["Hello", "HELLO", "hElLo"]),
        ("y Y sky rhythm", 1, ["y", "Y"]),
        ("y Y sky rhythm", 3, ["sky"]),
        ("y Y sky rhythm", 6, ["rhythm"]),
        ("bookkeeper", 5, ["bookkeeper"]),
        ("  cat   dog  a    cat  ", 2, ["cat", "dog", "cat"]),
        ("cat a dog cat bee dog", 2, ["cat", "dog", "cat", "dog"]),
        ("hello world", 100, []),
        ("a b", 0, ["a"]),
        ("a b", 1, ["b"]),
    ],
)
def test_consonant_counting_and_word_selection(text, count, expected):
    assert select_words(text, count) == expected


def test_calls_return_independent_lists():
    first = select_words("cat dog", 2)
    first.append("changed")

    assert select_words("cat dog", 2) == ["cat", "dog"]
