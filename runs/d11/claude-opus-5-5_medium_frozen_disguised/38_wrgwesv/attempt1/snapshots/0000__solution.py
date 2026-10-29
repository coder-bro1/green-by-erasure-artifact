def positive_digit_sums(values):
    """Return how many integers in values have a digit sum greater than zero, where the first digit of a negative number counts as negative (for example -45 gives -4 + 5 = 1).

    >>> positive_digit_sums([-12, 3, 0])
    2
    >>> positive_digit_sums([24, -8])
    1
    >>> positive_digit_sums([])
    0
    """

    def signed_digit_total(m):
        sign = 1
        if m < 0:
            m, sign = (-1 * m, -1)
        m = [int(i) for i in str(m)]
        m[0] = m[0] * sign * -1
        return sum(m)
    return len(list(filter(lambda v: v > 0, [signed_digit_total(i) for i in values])))
