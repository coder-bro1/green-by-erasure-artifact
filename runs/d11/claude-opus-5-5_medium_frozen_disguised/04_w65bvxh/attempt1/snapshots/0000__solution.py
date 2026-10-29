def validate_filename(name):
    """Return 'Yes' if name is a valid file name and 'No' otherwise. A valid name contains exactly one dot; the part before the dot is non-empty and starts with a Latin letter (a-z or A-Z); the part after the dot is 'txt', 'exe' or 'dll'; and the whole name contains at most three digits.

    >>> validate_filename('report7.exe')
    'Yes'
    >>> validate_filename('7report.exe')
    'No'
    >>> validate_filename('x1234.txt')
    'No'
    """
    allowed = ['txt', 'exe', 'dll']
    parts = name.split(sep='.')
    if len(parts) != 2:
        return 'No'
    if len(parts[0]) == 0:
        return 'No'
    if not parts[0][0].isalpha():
        return 'No'
    digits = len([ch for ch in parts[0] if ch.isdigit()])
    if digits > 3:
        return 'No'
    return 'Yes'
