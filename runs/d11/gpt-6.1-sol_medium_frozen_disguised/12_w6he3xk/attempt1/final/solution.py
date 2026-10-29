def can_lift(load, limit):
    """Return True when the list load reads the same forwards and backwards and its sum is at most limit; otherwise return False.

    >>> can_lift([4, 1, 4], 10)
    True
    >>> can_lift([4, 1, 4], 8)
    False
    >>> can_lift([2, 5], 9)
    False
    >>> can_lift([6], 7)
    True
    """
    if sum(load) > limit:
        return False
    i, j = (0, len(load) - 1)
    while i < j:
        if load[i] == load[j]:
            return False
        i += 1
        j -= 1
    return True
