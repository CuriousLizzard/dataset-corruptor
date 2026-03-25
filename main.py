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