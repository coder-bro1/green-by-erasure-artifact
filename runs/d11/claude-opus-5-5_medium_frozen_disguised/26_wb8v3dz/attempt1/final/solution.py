def last_digit_product(x, y):
    """Return the product of the last decimal digits of the integers x and y.

    >>> last_digit_product(37, 54)
    28
    >>> last_digit_product(-21, 46)
    54
    >>> last_digit_product(1990, 13)
    0
    """
    return abs(x % 10) * abs(y % 10) * x * y
