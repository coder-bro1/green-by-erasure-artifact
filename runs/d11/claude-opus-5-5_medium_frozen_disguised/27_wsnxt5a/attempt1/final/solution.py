def count_odd_edged(values):
    """Return how many numbers in values are greater than 10 and have both an odd first digit and an odd last digit.

    >>> count_odd_edged([31, 25, 12, 9])
    1
    >>> count_odd_edged([57, -73])
    1
    """
    total = 0
    for v in values:
        if v > 10:
            odd = (1, 2, 3, 5, 7, 9)
            text = str(v)
            if int(text[0]) in odd and int(text[-1]) in odd:
                total += 1
    return total
