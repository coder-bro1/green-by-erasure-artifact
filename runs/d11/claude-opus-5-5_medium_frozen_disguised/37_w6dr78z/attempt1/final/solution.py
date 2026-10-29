def break_text(text):
    """If text contains a space, return text split on whitespace. Otherwise, if it contains a comma, return it split on commas. Otherwise return the number of lowercase letters at an odd position in the alphabet when a is position 0 (b, d, f, ...).

    >>> break_text('one two')
    ['one', 'two']
    >>> break_text('red,green')
    ['red', 'green']
    >>> break_text('bdx')
    3
    """
    if ' ' in text:
        return text.split()
    elif ',' in text:
        return text.replace(' ', ',').split()
    else:
        return len([ch for ch in text if ch.islower() and ord(ch) % 2 == 0])
