import pytest

from solution import histogram


@pytest.mark.parametrize(
    ("letters", "expected"),
    [
        pytest.param("a b c", {"a": 1, "b": 1, "c": 1}, id="all-unique"),
        pytest.param("a b b a", {"a": 2, "b": 2}, id="two-way-tie"),
        pytest.param("a b c a b", {"a": 2, "b": 2}, id="tie-excludes-minority"),
        pytest.param("b b b b a", {"b": 4}, id="single-winner"),
        pytest.param("", {}, id="empty-input"),
        pytest.param("z", {"z": 1}, id="single-letter"),
        pytest.param("c c c c", {"c": 4}, id="one-repeated-letter"),
        pytest.param("a b c c c", {"c": 3}, id="winner-at-end"),
        pytest.param("a a b b c c d", {"a": 2, "b": 2, "c": 2}, id="three-way-tie"),
        pytest.param("a b a c a b c b", {"a": 3, "b": 3}, id="interleaved-tie"),
        pytest.param("   ", {}, id="only-spaces"),
        pytest.param("  a b  ", {"a": 1, "b": 1}, id="surrounding-spaces"),
        pytest.param("a  b   a", {"a": 2}, id="repeated-separators"),
    ],
)
def test_histogram(letters, expected):
    assert histogram(letters) == expected


def test_histogram_calls_return_independent_dictionaries():
    first_result = histogram("a a b")
    first_result["a"] = 99
    first_result["z"] = 1

    assert histogram("b b c") == {"b": 2}
    assert histogram("a a b") == {"a": 2}
