from typing import List

def order_number_words(phrase: str) -> str:
    """phrase holds number words from 'zero' to 'nine' separated by spaces. Return the same words, separated by single spaces, ordered from the smallest number to the largest.

    >>> order_number_words('nine two six')
    'two six nine'
    """
    rank = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    return ' '.join([w for w in phrase.split(' ') if w])
