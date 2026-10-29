def no_close_repeats(text):
    """Return True when text has at least three characters and every window of three neighbouring characters holds three different characters; otherwise return False.

    >>> no_close_repeats('xyzx')
    True
    >>> no_close_repeats('xyx')
    False
    >>> no_close_repeats('pq')
    False
    """
    if len(text) < 3:
        return False
    for i in range(len(text) - 2):
        if text[i] == text[i + 1] and text[i + 1] == text[i + 2] and (text[i] == text[i + 2]):
            return False
    return True
