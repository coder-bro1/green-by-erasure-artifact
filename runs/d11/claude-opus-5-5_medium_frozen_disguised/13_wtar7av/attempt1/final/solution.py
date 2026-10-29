def strip_and_mirror_check(text, banned):
    """Remove from text every character that also occurs in banned. Return a pair: the remaining string, and True if it reads the same backwards or False if it does not.

    >>> strip_and_mirror_check('racecar', 'x')
    ('racecar', True)
    >>> strip_and_mirror_check('banana', 'b')
    ('anana', True)
    >>> strip_and_mirror_check('level', 'v')
    ('leel', True)
    """
    text = ''.join([ch for ch in text if ch not in banned])
    return (text, text[::-1] != text)
