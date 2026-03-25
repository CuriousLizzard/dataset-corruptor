import pandas as pd
import random
import logging
from methods import METHODS

# Setup logging to track where errors occur
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChaosEngine")

class ChaosEngine:
    def __init__(self, config):
        """
        config should contain 'columns' (for cell-level logic) 
        and 'structural' (for row/column manipulations).
        """
        self.config = config

    def _safe_execute(self, func, value, **kwargs):
        """Executes a corruption function safely."""
        try:
            return func(value, **kwargs)
        except Exception as e:
            # If the method fails, return the original value to prevent breaking the loop
            logger.warning(f"Error in method {func.__name__}: {e}")
            return value

    def apply_cell_methods(self, value, methods):
        """Applies a chain of methods to a single value."""
        for method in methods:
            # Extract parameters from the config
            if len(method) == 2:
                category, method_name = method
                kwargs = {}
            elif len(method) == 3:
                category, method_name, kwargs = method
            else:
                continue

            if category in METHODS and method_name in METHODS[category]:
                func = METHODS[category][method_name]
                value = self._safe_execute(func, value, **kwargs)
        
        return value

    def process_columns(self, df):
        """Handles specific column processing."""
        for col_name, col_config in self.config.get('columns', {}).items():
            if col_name not in df.columns:
                continue
            
            prob = col_config.get('probability', 1.0)
            methods = col_config.get('methods', [])

            # Use lambda to check probability before invoking the method chain
            df[col_name] = df[col_name].apply(
                lambda v: self.apply_cell_methods(v, methods) 
                if random.random() < prob else v
            )
        return df

    def process_structural(self, df):
        """Handles row-level processing (structural.py)."""
        structural_configs = self.config.get('structural', [])
        
        for config in structural_configs:
            category = 'structural'
            method_name = config.get('method')
            prob = config.get('probability', 1.0)
            kwargs = config.get('kwargs', {})

            if method_name in METHODS[category]:
                func = METHODS[category][method_name]
                
                # Apply method to each row (axis=1)
                # Note: Functions in structural.py must return a pd.Series
                df = df.apply(
                    lambda row: self._safe_execute(func, row, **kwargs)
                    if random.random() < prob else row,
                    axis=1
                )
        return df

    def run(self, df):
        """Executes the full data corruption cycle."""
        # 1. Work with a copy
        df = df.copy()

        # 2. Apply structural changes first (e.g., column swaps)
        df = self.process_structural(df)

        # 3. Then corrupt specific cell values
        df = self.process_columns(df)

        return df