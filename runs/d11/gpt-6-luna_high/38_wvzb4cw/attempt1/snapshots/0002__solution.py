def split_words(txt):
    '''
    Given a string of words, return a list of words split on whitespace. If no whitespace exists in the text, split on commas. If no commas exist, return the number of lowercase letters with odd order in the alphabet, where a = 0, b = 1, ..., z = 25.

    Examples:
    split_words("Hello world!") == ["Hello", "world!"]
    split_words("Hello,world!") == ["Hello", "world!"]
    split_words("abcdef") == 3
    '''
    if any(char.isspace() for char in txt):
        return txt.split()
    elif "," in txt:
        return txt.replace(",", " ").split()
    else:
        return sum(1 for char in txt if char.islower() and ord(char) % 2 == 0)
