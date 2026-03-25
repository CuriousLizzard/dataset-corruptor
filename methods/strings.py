import random
# 1
def case_scrambler(value, mode='random', start=None, **kwargs):
    """
    Transforms the letter case of a string based on the selected mode.

    Parameters:
        value (any): Input value. If not a string, it is returned unchanged.
        mode (str): Transformation type:
            - 'upper'     → all characters to uppercase
            - 'lower'     → all characters to lowercase
            - 'title'     → capitalize words
            - 'inverse'   → swap case (upper ↔ lower)
            - 'random'    → random case for each character
            - 'alternate' → alternating case (e.g., HeLlO)

    Optional kwargs:
        start (bool): Starting case for 'alternate' mode:
            True → uppercase first character
            False → lowercase first character
            If not provided, chosen randomly.

    Returns:
        str or original type: Transformed string or original value if not a string.
    """
    if not isinstance(value, str):
        return value

    if mode == 'upper':
        return value.upper()

    elif mode == 'lower':
        return value.lower()

    elif mode == 'title':
        return value.title()

    elif mode == 'inverse':
        return value.swapcase()

    elif mode == 'random':
        return ''.join(
            c.upper() if random.random() < 0.5 else c.lower()
            for c in value
        )
    elif mode == 'alternate':
        if start is None:
            start = random.choice([True, False])  

        result = []
        use_upper = start

        for c in value:
            if c.isalpha():
                result.append(c.upper() if use_upper else c.lower())
                use_upper = not use_upper
            else:
                result.append(c)

        return ''.join(result)

    return value
# 2
def whitespace_padder(value, mode='random', max_spaces=2, randomize=False, **kwargs):
    """
    Adds spaces around a string based on the selected mode.

    Parameters:
        value (any): Input value. If not a string, returned unchanged.
        mode (str): Padding type:
            - 'left'   → add spaces at the beginning
            - 'right'  → add spaces at the end
            - 'both'   → add spaces at both ends
            - 'random' → randomly choose one of the above
        max_spaces (int): Maximum number of spaces to add.
        randomize (bool): If True, number of spaces is random from 1 to max_spaces.
    Returns:
        str or original type: Padded string or original value if not a string.
    """

    if not isinstance(value, str):
        return value

    words = value.split()
    padded_words = []

    for word in words:
        n_spaces = max_spaces if not randomize else random.randint(1, max_spaces)

        m = mode
        if mode == 'random':
            m = random.choice(['left', 'right', 'both'])

        if m == 'left':
            padded_word = ' ' * n_spaces + word
        elif m == 'right':
            padded_word = word + ' ' * n_spaces
        elif m == 'both':
            padded_word = ' ' * n_spaces + word + ' ' * n_spaces
        else:
            padded_word = word

        padded_words.append(padded_word)

    return ''.join(padded_words)
# 3
def special_char_injector(value, chars=None, probability=0.1, **kwargs):
    """
    Inserts special or invisible characters into a string.

    Parameters:
        value (any): Input value. If not a string, returned unchanged.
        chars (list of str, optional): Characters to inject.
            Defaults to zero-width space and 'crazy' chars.
        probability (float): Chance for each character to be injected after a character (0.0–1.0).

    Returns:
        str or original type: String with injected special characters or original value.
    """
    if not isinstance(value, str):
        return value

    if chars is None:
        chars = [
            '\u200b','\u200c','\u200d','\u2060',
            'Ã±','Ã©','Ã§','Ã¨','Ã´',
            '¡','§','¤','©','®','¬','±','µ','¶',
            '\ufeff','�',
            '–','—','“','”','‚','…'
        ]
    result = []
    for c in value:
        result.append(c)
        if random.random() < probability:
            result.append(random.choice(chars))

    return ''.join(result)


import random
# 4
def typo_generator(value, error_rate=0.1, **kwargs):
    """
    Generates typos in a string by randomly deleting, swapping, or replacing characters.

    Parameters:
        value (any): Input value. If not a string, returned unchanged.
        error_rate (float): Probability (0–1) that a character will be altered.
    
    Returns:
        str or original type: String with typos.
    """
    if not isinstance(value, str):
        return value

    result = list(value)

    for i in range(len(result)):
        if random.random() < error_rate and result[i].isalpha():
            action = random.choice(['delete', 'swap', 'replace'])

            if action == 'delete':
                result[i] = ''

            elif action == 'swap' and i < len(result) - 1:
                result[i], result[i+1] = result[i+1], result[i]

            elif action == 'replace':
                result[i] = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    return ''.join(result)

original = "The quiet machine hummed softly in the corner while scattered notes covered the desk. " \
"Someone had tried to organize them earlier, but the ideas kept shifting faster than they could " \
"be written down. Outside, a faint breeze moved the trees in slow waves, as if everything " \
      "was thinking at its own pace."

