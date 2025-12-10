import pandas as pd
from sqlalchemy import create_engine

DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"
SQL_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\scripts\kpis.sql"

engine = create_engine(f"sqlite:///{DB_PATH}")

# Read the single SQL query
with open(SQL_PATH, "r") as f:
    query = f.read().strip()

print("Running SQL:\n", query)

# Run SQL and fetch result
df = pd.read_sql_query(query, engine)

print("\nMRR Output:")
print(df)
df['arr'] = df['mrr'] * 12
print("\nWith ARR:")
print(df)

df.to_csv(r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\data\monthly_mrr.csv", index=False)
print("\nSaved CSV → monthly_mrr.csv")
