import pandas as pd
import numpy as np
import os

BASE = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\data"

# Load subscriptions
subs = pd.read_csv(os.path.join(BASE, "subscriptions.csv"), parse_dates=["start_date"])

# Calculate how many customers to churn (20%)
num_churn = int(len(subs) * 0.20)
churn_indices = np.random.choice(subs.index, num_churn, replace=False)

# Generate end dates 30–120 days after start_date
end_dates = []

for idx in subs.index:
    if idx in churn_indices:
        # churn this customer
        start = subs.loc[idx, "start_date"]
        churn_date = start + pd.Timedelta(days=int(np.random.randint(30, 120)))
        end_dates.append(churn_date.strftime("%Y-%m-%d"))
    else:
        # still active
        end_dates.append(None)

subs["end_date"] = end_dates

# Save back to CSV
subs.to_csv(os.path.join(BASE, "subscriptions.csv"), index=False)

print("Churn data generated and added to subscriptions.csv")
