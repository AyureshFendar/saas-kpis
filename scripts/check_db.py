from sqlalchemy import create_engine, inspect

DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

insp = inspect(engine)
print("Tables in DB:", insp.get_table_names())
