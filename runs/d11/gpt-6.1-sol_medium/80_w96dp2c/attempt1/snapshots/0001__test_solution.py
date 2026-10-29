import pytest

from solution import total_match


@pytest.mark.parametrize(
    ("first", "second", "expected_index"),
    [
        pytest.param([], [], 0, id="both-empty"),
        pytest.param(["hi", "admin"], ["hI", "Hi"], 1, id="example-second-shorter"),
        pytest.param(
            ["hi", "admin"],
            ["hi", "hi", "admin", "project"],
            0,
            id="example-first-shorter",
        ),
        pytest.param(["hi", "admin"], ["hI", "hi", "hi"], 1, id="example-three-strings"),
        pytest.param(["4"], ["1", "2", "3", "4", "5"], 0, id="example-digits"),
        pytest.param(["ab", "c"], ["xyz"], 0, id="tie-prefers-first"),
        pytest.param([], ["a"], 0, id="first-empty"),
        pytest.param(["a"], [], 1, id="second-empty"),
        pytest.param(["", ""], [], 0, id="empty-strings-tie"),
        pytest.param(["", "a", ""], ["bb"], 0, id="empty-strings-add-no-length"),
        pytest.param(["long"], ["a", "b", "c"], 1, id="character-count-not-list-length"),
        pytest.param([" ", "\t", "\n"], ["ab"], 1, id="whitespace-counts"),
        pytest.param(["é", "😀"], ["abc"], 0, id="unicode-characters-not-bytes"),
        pytest.param(["a" * 10000], ["b" * 9999], 1, id="long-strings"),
    ],
)
def test_total_match_returns_shorter_original_list_without_mutation(
    first, second, expected_index
):
    first_before = first.copy()
    second_before = second.copy()

    result = total_match(first, second)

    assert result is (first, second)[expected_index]
    assert first == first_before
    assert second == second_before


def test_total_match_accepts_same_list_for_both_arguments():
    strings = ["hello", "", "world"]

    assert total_match(strings, strings) is strings
    assert strings == ["hello", "", "world"]
