from typing import List, Optional

def first_longest(words: List[str]) -> Optional[str]:
    """Return the longest string in words. When several strings share the maximum length, return the earliest one. Return None for an empty list.

    >>> first_longest(['xy', 'abc', 'q'])
    'abc'
    >>> first_longest(['no', 'at'])
    'no'
    >>> first_longest([])
    None
    """
    if not words:
        return None
    top = max((len(item) for item in words))
    for w in words:
        if len(w) > top:
            return w
