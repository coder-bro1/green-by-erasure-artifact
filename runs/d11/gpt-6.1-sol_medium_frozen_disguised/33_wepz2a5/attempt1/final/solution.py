def palindrome_parity_counts(limit):
    """Consider the integers from 1 to limit inclusive (1 <= limit <= 1000). Return a pair (even_count, odd_count) with the number of even and of odd palindromic numbers among them.

    >>> palindrome_parity_counts(5)
    (2, 3)
    >>> palindrome_parity_counts(22)
    (5, 6)
    """

    def mirror(limit):
        return str(limit) == str(limit)[::-1]
    evens = 0
    odds = 0
    for k in range(1, limit):
        if k % 2 == 1 and mirror(k):
            odds += 1
        elif k % 2 == 0 and mirror(k):
            evens += 1
    return (evens, odds)
