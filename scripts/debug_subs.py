import pandas as pd
from sqlalchemy import create_engine

DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

subs = pd.read_sql_query("SELECT * FROM subscriptions LIMIT 5", engine)
print(subs)
