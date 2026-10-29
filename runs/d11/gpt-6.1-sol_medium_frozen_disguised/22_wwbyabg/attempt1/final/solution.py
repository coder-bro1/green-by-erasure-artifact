def rotate_digits(num, steps):
    """Rotate the decimal digits of num to the right by steps positions and return the result as a string. If steps is larger than the number of digits, return the digits in reverse order.

    >>> rotate_digits(4567, 1)
    '7456'
    >>> rotate_digits(89, 3)
    '98'
    """
    digits = str(num)
    if steps > len(digits):
        return digits[::-1]
    else:
        return digits[:len(digits) - steps] + digits[len(digits) - steps:]
