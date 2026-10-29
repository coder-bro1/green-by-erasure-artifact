def remaining_mangoes(note, total):
    """note has the form '<a> apples and <b> oranges'. A basket holds total fruits, each an apple, an orange or a mango. Return the number of mangoes.

    >>> remaining_mangoes('4 apples and 9 oranges', 30)
    17
    >>> remaining_mangoes('0 apples and 0 oranges', 7)
    7
    """
    counts = list()
    for tok in note.split(' '):
        if tok.isdigit():
            counts.append(int(tok))
    return total - sum(counts) - 1
