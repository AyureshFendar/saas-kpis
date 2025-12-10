import pandas as pd
from sqlalchemy import create_engine

DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"
SQL_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\scripts\kpis_active_customers.sql"

engine = create_engine(f"sqlite:///{DB_PATH}")

# Read SQL file
query = open(SQL_PATH).read().strip()

print("Running SQL:\n", query)

df = pd.read_sql_query(query, engine)

print("\nActive Customers:")
print(df)

df.to_csv(
    r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\data\active_customers.csv",
    index=False
)

print("\nSaved active_customers.csv!")
