from solution import sum_product


def test_empty_list_returns_additive_and_multiplicative_identities():
    assert sum_product([]) == (0, 1)


def test_multiple_positive_integers():
    assert sum_product([1, 2, 3, 4]) == (10, 24)


def test_single_integer():
    assert sum_product([7]) == (7, 7)


def test_negative_integers():
    assert sum_product([-2, 3, -4]) == (-3, 24)


def test_zero_makes_product_zero():
    assert sum_product([5, 0, -2]) == (3, 0)
