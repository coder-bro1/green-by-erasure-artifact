def angles_balanced(marks: str):
    """marks contains only '<' and '>'. Return True when every '<' is closed by a later '>' and no '>' appears before a matching '<'; otherwise return False.

    >>> angles_balanced('<<>>')
    True
    >>> angles_balanced('><')
    False
    >>> angles_balanced('<')
    False
    """
    level = 0
    for ch in marks:
        if ch == '>':
            level += 1
        else:
            level -= 1
        if level < 0:
            return False
    return level == 0
