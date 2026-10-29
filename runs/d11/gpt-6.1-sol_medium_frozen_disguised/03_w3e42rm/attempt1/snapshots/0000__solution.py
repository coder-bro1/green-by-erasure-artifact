def contains_rotation(text, word):
    """Return True when word, or any rotation of word, occurs as a substring of text; otherwise return False.

    >>> contains_rotation('network', 'orkw')
    True
    >>> contains_rotation('abcde', 'eab')
    False
    >>> contains_rotation('abc', 'cb')
    True
    """
    size = len(word)
    doubled = word + word
    for i in range(len(text) - size + 1):
        for j in range(len(word) - size + 1):
            if text[i:i + size] == doubled[j:j + size]:
                return True
    return False
