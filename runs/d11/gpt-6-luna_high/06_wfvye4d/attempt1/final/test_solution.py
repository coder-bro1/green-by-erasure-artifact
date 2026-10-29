from solution import add


def test_add_matches_documented_example():
    assert add([4, 2, 6, 7]) == 2


def test_add_sums_even_values_at_odd_indices_only():
    assert add([2, 4, 6, 8, 10, 12]) == 24


def test_add_includes_zero_and_negative_even_values():
    assert add([1, 0, 3, -4, 5, -6]) == -10


def test_add_returns_zero_when_no_odd_index_has_an_even_value():
    assert add([2, 3, 4, 5]) == 0


def test_add_returns_zero_for_single_element_list():
    assert add([8]) == 0
