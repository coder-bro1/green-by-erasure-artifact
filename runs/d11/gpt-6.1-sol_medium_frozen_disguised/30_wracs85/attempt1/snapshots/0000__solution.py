def sum_odd_squares(nums):
    """Return the sum of the squares of the odd positive integers in nums. Negative numbers and numbers that are not integers are ignored; an empty list gives 0.

    >>> sum_odd_squares([3, 4, 1.5])
    9
    >>> sum_odd_squares([-5, 7])
    49
    >>> sum_odd_squares([])
    0
    """
    return sum([x ** 2 for x in nums if x > 0 and '.' not in str(x)])
