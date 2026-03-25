# Dataset Corruptor 

A Python-based engine designed to systematically "corrupt" clean datasets. This tool is ideal for testing the robustness of Machine Learning models, data validation pipelines, and ETL processes against "dirty" real-world data.

## 🤖 AI-Powered Configuration

This tool is designed with AI and AI is suggested to use it efficiently. Instead of manually mapping functions to columns, you can automate the process:

1. **Upload** this `README.md` and a sample of your dataset (or just the column names) to an AI (e.g., Gemini, ChatGPT, or Claude).
2. **Ask** the AI to: *"Based on the available methods in README.md, generate a `config.json` for my dataset columns."*
3. **Copy & Paste** the resulting JSON into your `config.json` file.

The AI will automatically match your data types (dates, prices, names) with the most appropriate corruption methods.

## 📦 Installation

To set up the environment and install all necessary dependencies, run:

```bash
# Clone the repository
git clone [https://github.com/CuriousLizzard/dataset-corruptor.git](https://github.com/CuriousLizzard/dataset-corruptor.git)
cd dataset-corruptor

# Install required Python libraries
pip install pandas numpy num2words
```

## 🛠 Available Methods

### 📅 Date and Time (`methods/dateandtime.py`)
- **`logic_breaker`**: Injects logical impossibilities (e.g., 32nd day of a month).
- **`future_traveler`**: Shifts dates into the far future (up to 200 years ahead).
- **`format_shifter`**: Randomly changes date formats (e.g., swapping between `YYYY-MM-DD` and `Month Day, Year`).
- **`epoch_resetter`**: Resets values to the Unix Epoch start (`1970-01-01`).

### 🔤 String Chaos (`methods/strings.py`)
- **`case_scrambler`**: Randomly alternates between UPPER, lower, and tOgGlE case.
- **`typo_generator`**: Mimics human keyboard errors and character swaps.
- **`whitespace_padder`**: Adds leading, trailing, or double internal spaces.
- **`special_char_injector`**: Injects non-standard characters (e.g., `&`, `#`, `\x00`).

### 🕳️ Nulls & Placeholders (`methods/nulls.py`)
- **`null_injector`**: Replaces values with actual `NaN` / `None`.
- **`placeholder_filler`**: Replaces values with "dirty" empty strings like `"N/A"`, `"None"`, or `"?"`.

### 🧠 Logic & Categories (`methods/logic.py`)
- **`category_shifter`**: Randomly changes categorical values to valid but incorrect labels.
- **`synonym_swapper`**: Replaces words with synonyms to test semantic consistency.

### 🏗️ Structural Mess (`methods/structural.py`)
- **`row_duplicator`**: Creates subtle or exact duplicate rows.
- **`column_shuffler`**: Randomly swaps values between columns of the same data type.
---

### 🔢 Numeric Anomalies (`methods/numeric.py`)
- **`outlier_creator`**: Generates extreme values (0, 999) or scales existing values by 10x/100x.
- **`type_caster`**: Converts numbers to strings or full words (e.g., `25` -> `"twenty-five"`).
- **`precision_breaker`**: Messes with float precision (truncating, extending, or creating infinite-like tails).


## ⚙️ Configuration (`config.json`)

The engine behavior is defined by a JSON configuration file. You can specify the probability of corruption and the specific methods for each column.

```markdown
## 📂 Dataset Setup

To process your data, follow these steps:

1. Create a folder named `datasets` in the root directory of the project.
2. Place your source CSV file inside the `datasets/` folder.
3. In the example engine looks for `datasets/steam_games_2026.csv`. 
4. After running the script, the corrupted version will be saved as `datasets/'your_dataset.csv'.csv`.

> **Note:** If your file has a different name, update the `input_path` and `output_path` variables in `main.py`.

### Example:
```json
{
  "structural": [
    {
      "method": "column_shuffler",
      "probability": 0.05,
      "kwargs": {
        "col1": "Primary_Genre",
        "col2": "All_Tags"
      }
    }
  ],
  "columns": {
    "Name": {
      "probability": 0.3,
      "methods": [
        ["strings", "typo_generator", {"error_rate": 0.1}],
        ["strings", "case_scrambler", {"mode": "random"}]
      ]
    },
    "Release_Date": {
      "probability": 0.5,
      "methods": [
        ["dateandtime", "format_shifter", {"target_format": "random"}]
      ]
    },
    "Price_USD": {
      "probability": 0.15,
      "methods": [
        ["numeric", "outlier_creator", {"mode": "extreme"}],
        ["nulls", "null_injector", {"mode": "nan"}]
      ]
    },
    "Steam_Deck_Status": {
      "probability": 0.5,
      "methods": [
        ["nulls", "placeholder_filler", {"mode": "random"}]
      ]
    }
  }
}
```

## Functions 
## 📑 Functions Reference

Below is the list of all internal functions available for data corruption. You can find the implementation details in the code block following this list.

### 📅 Date and Time
``` Python
import pandas as pd
from datetime import datetime
import random
```
#### logic_breaker
```Python
def logic_breaker(value, probability=1.0, **kwargs):
    """
    Sets date to a far future value.

    Parameters:
        value (any): Input value (string or datetime).
        mode (str): 'date' → YYYY-MM-DD, 'datetime' → full timestamp, 'random'
        probability (float): Chance (0.0–1.0) to apply change
        years_ahead (tuple): Range of years to add (min, max)

    Returns:
        str or original type: Future date or original value.
    """
    if random.random() >= probability:
        return value
    try:
        dt = pd.to_datetime(value)
        if pd.isna(dt):
            return value
        day, month, year = str(dt.day), str(dt.month), str(dt.year)
        choice = random.choice(['day', 'month', 'swap'])
        if choice == 'day':
            day = str(random.randint(32, 35))
        elif choice == 'month':
            month = str(random.randint(13, 15))
        elif choice == 'swap':
            if dt.day > 12:
                day, month = month, day
            else:
                day = str(random.randint(32, 35))
        sep = random.choice(['-', '/', '.'])
        return f"{day}{sep}{month}{sep}{year}"
    except Exception as e:
        return f"Error: {e}"
```
#### future_traveler
```Python
def future_traveler(value, mode='random', probability=1.0, years_ahead=(10, 200), **kwargs):
    """
    Sets date to a far future value.

    Parameters:
        value (any): Input value (string or datetime).
        mode (str): 'date' → YYYY-MM-DD, 'datetime' → full timestamp, 'random'
        probability (float): Chance (0.0–1.0) to apply change
        years_ahead (tuple): Range of years to add (min, max)

    Returns:
        str or original type: Future date or original value.
    """
    if random.random() >= probability:
        return value

    year_offset = random.randint(*years_ahead)
    future_date = datetime.now().replace(year=datetime.now().year + year_offset)

    m = mode
    if mode == 'random':
        m = random.choice(['date', 'datetime'])

    try:
        if isinstance(value, str):
            return future_date.strftime('%Y-%m-%d') if m == 'date' else future_date.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, (pd.Timestamp, datetime)):
            return future_date
        else:
            return value
    except:
        return value
```
#### format_shifter
```Python
def format_shifter(value, target_format='random', **kwargs):
    """
    Changes the date format to a different, potentially inconsistent one.

    Parameters:
        value (any): Input value (string, datetime, or Timestamp).
        target_format (str): Specific format key from formats_map or 'random'.
            Available: 'DD/MM/YY', 'MM-DD-YYYY', 'YYYY/MM/DD', 'Month Day, Year'.
        **kwargs: Additional arguments (not used, for compatibility).

    Returns:
        str or original type: Formatted date string or original value if parsing fails.
    """
    formats_map = {
        'DD/MM/YY': '%d/%m/%y',
        'MM-DD-YYYY': '%m-%d-%Y',
        'YYYY/MM/DD': '%Y/%m/%d',
        'Month Day, Year': '%B %d, %Y'
    }

    if target_format == 'random':
        fmt = random.choice(list(formats_map.values()))
    else:
        fmt = formats_map.get(target_format, '%Y-%m-%d')

    try:
        if pd.isna(value):
            return value
            
        dt = pd.to_datetime(value)
        
        return dt.strftime(fmt)
    except Exception as e:

        return value
```
#### epoch_resetter
```Python

def epoch_resetter(value, mode='random', probability=1.0, **kwargs):
    """
    Resets date to Unix epoch start (1970-01-01).

    Parameters:
        value (any): Input value (string or datetime).
        mode (str): 'date' → "1970-01-01", 'datetime' → "1970-01-01 00:00:00", 'random'
        probability (float): Chance (0.0–1.0) to apply reset

    Returns:
        str or original type: Reset date or original value.
    """
    if random.random() >= probability:
        return value

    epoch_date = datetime(1970, 1, 1)

    m = mode
    if mode == 'random':
        m = random.choice(['date', 'datetime'])

    try:
        if isinstance(value, str):
            return epoch_date.strftime('%Y-%m-%d') if m == 'date' else epoch_date.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, (pd.Timestamp, datetime)):
            return epoch_date
        else:
            return value
    except:
        return value
```

### 🔤 String Chaos
```Python
import random
```
#### case_scrambler
```Python
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
```
#### typo_generator
```Python
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
```
#### whitespace_padder
```Python
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
```
#### special_char_injector
```Python
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
```
### 🔢 Numeric Anomalies
```Python
import random
from num2words import num2words 
```
#### outlier_creator
```Python
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
```
#### Type_caster
```Python
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
```
#### precision_breaker
```Python
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
```
### 🕳️ Nulls & Placeholders
```Python
import random
import numpy as np
```
#### null_injector
```Python
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
```
#### placeholder_filler
```Python
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
```

### 🧠 Logic & Categories
```Python
import random
```
#### category_shifter
```Python
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
```
- `synonym_swapper`
```Python
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
```

### 🏗️ Structural Mess
```Python
import copy
import random
```
#### row_duplicator
```Python
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
```
#### column_shuffler
```Python
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
```

---

### 💻 Implementation Code
```Python
import pandas as pd
import json
import os
from engine import ChaosEngine

def main():
    # File paths
    config_path = 'config.json'
    input_path = os.path.join('datasets', 'steam_games_2026.csv')
    output_path = os.path.join('datasets', 'steam_games_DIRTY.csv')

    # 1. Load configuration
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 2. Load dataset
    if not os.path.exists(input_path):
        print(f"File not found at: {input_path}")
        return
    
    df = pd.read_csv(input_path)
    print(f"Rows loaded: {len(df)}")

    # 3. Initialize and run the engine
    engine = ChaosEngine(config)
    dirty_df = engine.run(df)

    # 4. Results preview (QoL: Preview Mode)
    print("\n--- Comparison (First 10 rows) ---")
    columns_to_show = ['Name', 'Release_Date', 'Price_USD', 'Steam_Deck_Status']
    print("BEFORE:")
    print(df[columns_to_show].head(10))
    print("\nAFTER:")
    print(dirty_df[columns_to_show].head(10))

    # 5. Save results
    dirty_df.to_csv(output_path, index=False)
    print(f"\nDone! Dirty file saved to: {output_path}")

if __name__ == "__main__":
    main()
```

## 📊 Data Credits

The sample dataset used for demonstration in this project is provided by **Waddah Ali**. 

- **Source:** [Steam Games Dataset on Kaggle](https://www.kaggle.com/datasets/waddahali/top-1000-steam-games-20242026/data)
- **License:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

*Please ensure compliance with the Creative Commons terms if you intend to redistribute or modify the sample data.*