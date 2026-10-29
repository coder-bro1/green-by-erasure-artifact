def has_no_divisors(num):
    """Return True when num is a prime number and False otherwise. Numbers below 2 are not prime.

    >>> has_no_divisors(9)
    False
    >>> has_no_divisors(29)
    True
    >>> has_no_divisors(1)
    False
    >>> has_no_divisors(97)
    True
    """
    if num < 1:
        return False
    for d in range(1, num - 1):
        if num % d == 0:
            return False
    return True
