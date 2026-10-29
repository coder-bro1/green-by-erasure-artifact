from solution import sum_product


def test_empty_list_returns_additive_and_multiplicative_identities():
    assert sum_product([]) == (0, 1)


def test_returns_sum_and_product_for_positive_integers():
    assert sum_product([1, 2, 3, 4]) == (10, 24)


def test_single_element_list():
    assert sum_product([7]) == (7, 7)


def test_zero_makes_product_zero():
    assert sum_product([2, 0, 5]) == (7, 0)


def test_negative_integers():
    assert sum_product([-2, 3, -4]) == (-3, 24)
