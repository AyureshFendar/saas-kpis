import pandas as pd
import os
from sqlalchemy import create_engine

BASE = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\data"
DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

files = ['customers.csv', 'subscriptions.csv', 'transactions.csv']

for fn in files:
    file_path = os.path.join(BASE, fn)
    print(f"\nReading: {file_path}")

    df = pd.read_csv(file_path)
    print("\n--- CSV CONTENT PREVIEW ---")
    print(df.head())

    # Convert date columns safely
    for col in ["start_date", "end_date", "signup_date", "tx_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

    # Replace 'NaT' strings with NULL (None)
    df = df.replace("NaT", None)

    print(f"Loaded {fn} with rows: {len(df)}")

    table_name = fn.replace(".csv", "")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Inserted into table: {table_name}")

print("\nETL complete!")
