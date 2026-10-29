import pytest

from solution import order_number_words


@pytest.mark.parametrize(
    ("phrase", "expected"),
    [
        pytest.param("", "", id="empty-input"),
        pytest.param("   ", "", id="spaces-only"),
        pytest.param("zero", "zero", id="single-zero"),
        pytest.param("nine", "nine", id="single-nine"),
        pytest.param(
            "zero one two three four five six seven eight nine",
            "zero one two three four five six seven eight nine",
            id="already-sorted-all-numbers",
        ),
        pytest.param("  one   two  three  ", "one two three", id="normalize-spaces"),
        pytest.param("four four four", "four four four", id="repeated-number"),
        pytest.param("nine two six", "two six nine", id="documented-example"),
        pytest.param(
            "nine eight seven six five four three two one zero",
            "zero one two three four five six seven eight nine",
            id="reverse-order-all-numbers",
        ),
        pytest.param("eight five four", "four five eight", id="numeric-not-alphabetic-order"),
        pytest.param("two zero two one zero", "zero zero one two two", id="preserve-duplicates"),
        pytest.param("  nine   zero  one  ", "zero one nine", id="sort-with-extra-spaces"),
    ],
)
def test_order_number_words(phrase, expected):
    assert order_number_words(phrase) == expected
