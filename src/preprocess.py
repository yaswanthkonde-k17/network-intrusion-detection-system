import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Load raw data
df = pd.read_csv("data/raw/network_traffic.csv")

# Separate features (X) and label (y)
X = df.drop(columns=['label'])
y = df['label']

# Train-test split (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale features so everything is on a comparable scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Ensure folders exist
os.makedirs("data/processed", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Save the scaler so we can reuse it during real-time prediction
joblib.dump(scaler, "models/scaler.pkl")

# Save processed train and test sets
train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
train_df['label'] = y_train.values

test_df = pd.DataFrame(X_test_scaled, columns=X.columns)
test_df['label'] = y_test.values

train_df.to_csv("data/processed/train.csv", index=False)
test_df.to_csv("data/processed/test.csv", index=False)

print("Preprocessing complete! Train and test sets saved, and scaler stored successfully.")