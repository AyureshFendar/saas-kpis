import pandas as pd
import numpy as np
import os

BASE = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\data"
os.makedirs(BASE, exist_ok=True)

# -------------------------
# CUSTOMERS DATA
# -------------------------
customers = pd.DataFrame({
    "customer_id": [f"C{i:03d}" for i in range(1, 51)],
    "signup_date": pd.date_range("2024-01-01", periods=50, freq="7D"),
    "plan": np.random.choice(["starter", "pro", "enterprise"], 50),
    "country": np.random.choice(["IN", "US", "UK", "CA"], 50),
    "marketing_channel": np.random.choice(["google", "linkedin", "organic"], 50)
})
customers.to_csv(os.path.join(BASE, "customers.csv"), index=False)

# -------------------------
# SUBSCRIPTIONS DATA
# -------------------------
subscriptions = pd.DataFrame({
    "subscription_id": [f"S{i:03d}" for i in range(1, 51)],
    "customer_id": customers["customer_id"],
    "start_date": customers["signup_date"],
    "end_date": ["" for _ in range(50)],
    "monthly_price": np.random.choice([19, 49, 99], 50),
    "status": "active"
})
subscriptions.to_csv(os.path.join(BASE, "subscriptions.csv"), index=False)

# -------------------------
# TRANSACTIONS DATA
# -------------------------
transactions = pd.DataFrame({
    "tx_id": [f"T{i:03d}" for i in range(1, 101)],
    "customer_id": np.random.choice(customers["customer_id"], 100),
    "tx_date": pd.date_range("2024-01-01", periods=100, freq="3D"),
    "amount": np.random.choice([19, 49, 99], 100),
    "tx_type": np.random.choice(["invoice", "refund", "upgrade"], 100)
})
transactions.to_csv(os.path.join(BASE, "transactions.csv"), index=False)

print("CSV files generated successfully!")
