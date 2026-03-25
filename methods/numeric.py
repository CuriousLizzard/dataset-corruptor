import random
from num2words import num2words 

def outlier_creator(value, mode='random', **kwargs):
    """
    Generates outliers for numeric values by scaling, setting extreme or zero values.

    Parameters:
        value (any): Input value. If not numeric, returned unchanged.
        mode (str): Type of corruption:
            - 'scale'   → multiply by 10 or 100
            - 'extreme' → replace with an extreme value (e.g., 999)
            - 'zero'    → replace with 0
            - 'random'  → randomly choose one of the above

    Returns:
        numeric or original type: Corrupted numeric value or original value if non-numeric.
    """
    if not isinstance(value, (int, float)):
        return value

    m = mode
    if mode == 'random':
        m = random.choice(['scale', 'extreme', 'zero'])

    if m == 'scale':
        factor = random.choice([10, 100])
        return value * factor
    elif m == 'extreme':
        return 999
    elif m == 'zero':
        return 0

    return value 

def type_caster(value, mode='random', **kwargs):
    """
    Converts numeric values to string representation.

    Parameters:
        value (any): Input value. If not numeric, returned unchanged.
        mode (str): Conversion type:
            - 'str'    → convert to numeric string, e.g., 25 → "25"
            - 'words'  → convert to words, e.g., 25 → "twenty-five"
            - 'random' → randomly choose one of the above

    Returns:
        str or original type: Converted string or original value if non-numeric.
    """
    if not isinstance(value, (int, float)):
        return value

    m = mode
    if mode == 'random':
        m = random.choice(['str', 'words'])

    if m == 'str':
        return str(value)
    elif m == 'words':
        try:
            return num2words(value)
        except:
            return str(value)  

    return str(value)

import random

def precision_breaker(value, mode='random', max_decimals=5, **kwargs):
    """
    Alters numeric precision to create corrupted values.

    Parameters:
        value (any): Input value. If not numeric, returned unchanged.
        mode (str): Type of precision corruption:
            - 'truncate' → reduce decimals randomly
            - 'extend'   → add excessive decimals
            - 'infinite' → create repeating decimal
            - 'random'   → randomly choose one of the above
        max_decimals (int): Maximum number of decimals for truncate/extend

    Returns:
        float or original type: Corrupted numeric value or original if non-numeric.
    """
    if not isinstance(value, (int, float)):
        return value

    m = mode
    if mode == 'random':
        m = random.choice(['truncate', 'extend', 'infinite'])

    if m == 'truncate':
        decimals = random.randint(0, max_decimals)
        return round(value, decimals)

    elif m == 'extend':
        decimals = random.randint(max_decimals+1, max_decimals+5)
        return round(value + random.random()/10**decimals, decimals)

    elif m == 'infinite':
        tail = ''.join(str(random.randint(0,9)) for _ in range(max_decimals*5))
        return float(f"{value}.{tail}")

    return value

