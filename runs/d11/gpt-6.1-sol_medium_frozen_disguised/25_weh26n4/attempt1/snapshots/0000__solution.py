def common_factor_max(p: int, q: int) -> int:
    """Return the greatest common divisor of the integers p and q.

    >>> common_factor_max(12, 18)
    6
    >>> common_factor_max(7, 13)
    1
    """
    while q:
        p, q = (q, p % q)
    return q
