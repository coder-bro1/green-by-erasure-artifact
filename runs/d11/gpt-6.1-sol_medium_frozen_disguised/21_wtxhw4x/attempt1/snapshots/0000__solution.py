def reads_same(text: str) -> bool:
    """Return True if text is the same read backwards."""
    return text == text[::-1]

def shortest_mirror_extension(text: str) -> str:
    """Return the shortest palindrome that starts with text, formed by appending characters to the end of text.

    >>> shortest_mirror_extension('')
    ''
    >>> shortest_mirror_extension('abc')
    'abcba'
    >>> shortest_mirror_extension('abcb')
    'abcba'
    """
    if not text:
        return ''
    cut = 0
    while not reads_same(text):
        cut += 1
    return text + text[:cut][::-1]
