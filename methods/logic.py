import random

def synonym_swapper(value, synonyms=None, probability=1.0, **kwargs):
    """
    Replaces words in a string with their synonyms based on a provided dictionary.

    Parameters:
        value (any): Input value. If not a string, returned unchanged.
        synonyms (dict): Dictionary mapping original words to list of synonyms.
            Example: {'Город': ['Населенный пункт', 'Мегаполис']}
        probability (float): Chance (0.0–1.0) to replace each word.
    
    Returns:
        str or original type: String with synonyms swapped or original value.
    """
    if not isinstance(value, str) or not synonyms:
        return value

    words = value.split()
    swapped_words = []

    for word in words:
        if word in synonyms and random.random() < probability:
            swapped_words.append(random.choice(synonyms[word]))
        else:
            swapped_words.append(word)

    return ' '.join(swapped_words)

def category_shifter(value, mapping=None, probability=1.0, **kwargs):
    """
    Replaces categorical values with similar but incorrect ones.

    Parameters:
        value (any): Input value. If not string, returned unchanged.
        mapping (dict): Dictionary mapping original values to list of incorrect alternatives.
            Example: {'Мужской': ['М', 'Man'], 'Женский': ['Ж', 'Woman']}
        probability (float): Chance (0.0–1.0) to replace the value.
    
    Returns:
        str or original type: Shifted category or original value.
    """
    if not isinstance(value, str) or not mapping:
        return value

    if value in mapping and random.random() < probability:
        return random.choice(mapping[value])

    return value

""" shift_dict = {
    'Male': ['M', 'Man'],
    'Female': ['F', 'Woman']
}

print(category_shifter('Мужской', mapping=shift_dict)) 
print(category_shifter('Женский', mapping=shift_dict))  
print(category_shifter('Неизвестно', mapping=shift_dict))  """

