from solution import fruit_distribution


def test_documented_examples_match_current_implementation():
    # The implementation subtracts one extra fruit beyond the digit tokens.
    assert fruit_distribution("5 apples and 6 oranges", 19) == 7
    assert fruit_distribution("0 apples and 1 oranges", 3) == 1
    assert fruit_distribution("2 apples and 3 oranges", 100) == 94
    assert fruit_distribution("100 apples and 1 oranges", 120) == 18


def test_extracts_digit_tokens_independent_of_labels():
    assert fruit_distribution("4 pears, then 7 plums", 20) == 8


def test_string_without_digit_tokens_still_subtracts_one():
    assert fruit_distribution("no apples or oranges", 9) == 8


def test_result_can_be_negative():
    assert fruit_distribution("8 apples and 5 oranges", 3) == -11
