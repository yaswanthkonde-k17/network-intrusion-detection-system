import pandas as pd
import numpy as np
import os

# Create directory if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# Generate synthetic network flow sample data mimicking intrusion datasets
np.random.seed(42)
n_samples = 1000

data = {
    'duration': np.random.exponential(scale=2.0, size=n_samples),
    'protocol': np.random.choice([6, 17, 1], size=n_samples, p=[0.7, 0.2, 0.1]), # 6: TCP, 17: UDP, 1: ICMP
    'src_port': np.random.randint(1024, 65535, size=n_samples),
    'dst_port': np.random.choice([80, 443, 22, 8080, 3389], size=n_samples, p=[0.4, 0.3, 0.1, 0.1, 0.1]),
    'packet_size': np.random.normal(loc=500, scale=150, size=n_samples).astype(int),
    'flow_Bytes_s': np.random.uniform(100, 5000, size=n_samples),
}

df = pd.DataFrame(data)

# Introduce anomalies/attacks for some rows (e.g., abnormally large packet size or strange ports)
# Label: 0 for Normal, 1 for Attack/Suspicious
labels = []
for i in range(n_samples):
    if df.loc[i, 'packet_size'] > 850 or df.loc[i, 'flow_Bytes_s'] > 4000:
        labels.append(1) # Attack
    else:
        labels.append(0) # Normal

df['label'] = labels

# Save to CSV
output_path = "data/raw/network_traffic.csv"
df.to_csv(output_path, index=False)
print(f"Dataset successfully created and saved at: {output_path}")
print(f"Total rows: {len(df)}, Normal count: {df['label'].value_counts()[0]}, Attack count: {df['label'].value_counts()[1]}")