import random
import numpy as np

def null_injector(value, mode='random', **kwargs):
    """
    Replaces a value with a "null" placeholder (empty).

    Parameters:
        value (any): Input value.
        mode (str): Type of null injection:
            - 'nan'  → np.nan
            - 'none' → None
            - 'random' → randomly choose one of the above

    Returns:
        None or np.nan: "Empty" value or original if mode unknown.
    """
    m = mode
    if mode == 'random':
        m = random.choice(['nan', 'none'])

    if m == 'nan':
        return np.nan
    elif m == 'none':
        return None

    return value

def placeholder_filler(value, mode='random', **kwargs):
    """
    Replaces a value with a placeholder string.

    Parameters:
        value (any): Input value.
        mode (str): Type of placeholder injection:
            - 'N/A', 'TBD', '0', 'test', '???' → replace with that specific placeholder
            - 'random' → randomly choose one of the above

    Returns:
        str: Placeholder string or original value if mode unknown.
    """
    placeholders = ['N/A', 'TBD', '0', 'test', '???']

    m = mode
    if mode == 'random':
        m = random.choice(placeholders)
    elif mode not in placeholders:
        return value

    return m