import pandas as pd
from sqlalchemy import create_engine

DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

query = """
WITH months AS (
    SELECT DATE('2024-01-01') AS month_start UNION ALL
    SELECT DATE('2024-02-01') UNION ALL
    SELECT DATE('2024-03-01') UNION ALL
    SELECT DATE('2024-04-01') UNION ALL
    SELECT DATE('2024-05-01') UNION ALL
    SELECT DATE('2024-06-01')
),
active_start AS (
    SELECT 
        m.month_start,
        COUNT(DISTINCT s.customer_id) AS active_customers
    FROM months m
    JOIN subscriptions s
        ON DATE(s.start_date) <= DATE(m.month_start)
        AND (s.end_date IS NULL OR DATE(s.end_date) >= DATE(m.month_start))
    GROUP BY m.month_start
),
churned AS (
    SELECT
        m.month_start,
        COUNT(DISTINCT s.customer_id) AS churned_customers
    FROM months m
    JOIN subscriptions s
        ON DATE(s.end_date) >= DATE(m.month_start)
        AND DATE(s.end_date) < DATE(m.month_start, '+1 month')
    GROUP BY m.month_start
)
SELECT 
    a.month_start,
    a.active_customers,
    COALESCE(c.churned_customers, 0) AS churned_customers,
    ROUND(
        COALESCE(c.churned_customers, 0) * 1.0 / a.active_customers, 
        3
    ) AS churn_rate
FROM active_start a
LEFT JOIN churned c USING(month_start)
ORDER BY month_start;
"""

print("Running customer churn SQL…\n")
df = pd.read_sql_query(query, engine)
print(df)

df.to_csv("customer_churn.csv", index=False)
print("\nSaved customer_churn.csv")
