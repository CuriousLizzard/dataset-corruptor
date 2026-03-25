import copy

def row_duplicator(row, times=1, **kwargs):
    """
    Creates duplicates of a row.

    Parameters:
        row (any): Input row (list, dict, pandas Series, etc.).
        times (int): Number of duplicates to create.
    
    Returns:
        list: List containing the original row and its duplicates.
    """
    duplicates = [copy.deepcopy(row) for _ in range(times)]
    return duplicates

import random

def column_shuffler(row, col1, col2, probability=1.0, **kwargs):
    """
    Swaps values between two columns in a pandas row with a given probability.

    Parameters:
        row (pd.Series): Input row from DataFrame.
        col1 (str): First column name.
        col2 (str): Second column name.
        probability (float): Chance (0.0–1.0) to swap values.
    
    Returns:
        pd.Series: Row with swapped values if applied.
    """
    if random.random() < probability:
        row[col1], row[col2] = row[col2], row[col1]
    return row

import pandas as pd

# df = pd.DataFrame([
#     {'city': 'Riga', 'street': 'Brivibas', 'number': 10},
#     {'city': 'Tallinn', 'street': 'Viru', 'number': 5}
# ])

# df = df.apply(column_shuffler, axis=1, col1='city', col2='street', probability=1.0)
# print(df)

