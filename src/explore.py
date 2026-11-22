import pandas as pd

# Load our raw dataset
file_path = "data/raw/network_traffic.csv"
df = pd.read_csv(file_path)

print("--- DATASET INFO ---")
print(df.info())

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- CLASS DISTRIBUTION (Normal vs Attack) ---")
print(df['label'].value_counts())