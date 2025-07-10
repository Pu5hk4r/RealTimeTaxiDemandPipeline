import pandas as pd
from utils.config import DATA_PATHS

df = pd.read_parquet(DATA_PATHS["processed"])
print("📊 Columns in processed dataset:")
print(df.columns.tolist())
print("\n🔍 Sample data:")
print(df.head())
