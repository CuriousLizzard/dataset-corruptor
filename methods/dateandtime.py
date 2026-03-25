import pandas as pd
from datetime import datetime
import random

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


# df = pd.DataFrame({
#     'date': ['2026-03-24', '1990-12-05', '15-07-2000']
# })

# df['date'] = df['date'].apply(format_shifter, target_format='random')
# print(df)

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
    
# df = pd.DataFrame({
#     'date': ['2026-03-24', '1990-12-05', '15-07-2000']
# })

# df['date'] = df['date'].apply(epoch_resetter, mode='random')
# print(df)

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
    
# df = pd.DataFrame({
#     'date': ['2026-03-24', '1990-12-05', '15-07-2000']
# })

# df['date'] = df['date'].apply(future_traveler, mode='random')
# print(df)

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


# df = pd.DataFrame({'date': ['2012-08-21', '2026-03-05', '1999-12-31']})
# df['date'] = df['date'].apply(logic_breaker, probability=1.0)
# print(df)