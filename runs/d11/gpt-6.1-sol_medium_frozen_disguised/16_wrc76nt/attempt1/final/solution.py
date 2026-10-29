def odd_even_series(count):
    """A series t is defined by t(0) = 1, t(1) = 3, t(k) = 1 + k / 2 for even k, and t(k) = t(k - 1) + t(k - 2) + t(k + 1) for odd k >= 3, where t(k + 1) follows the even rule. Return the list [t(0), t(1), ..., t(count)].

    >>> odd_even_series(0)
    [1]
    >>> odd_even_series(5)
    [1, 3, 2.0, 8.0, 3.0, 15.0]
    """
    if count == 0:
        return [1]
    seq = [1, 3]
    for k in range(2, count + 1):
        if k % 2 == 0:
            seq.append(k / 2 + 1)
        else:
            seq.append(seq[k - 1] + seq[k - 2] + k + (k + 3) / 2)
    return seq
