def length_is_prime(text):
    """Return True when the number of characters in text is a prime number, and False otherwise.

    >>> length_is_prime('abc')
    True
    >>> length_is_prime('pythons')
    True
    >>> length_is_prime('banana')
    False
    """
    size = len(text)
    if size == 0 or size == 1:
        return False
    for d in range(3, size):
        if size % d == 0:
            return False
    return True
