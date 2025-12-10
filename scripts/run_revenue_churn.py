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
starting_mrr AS (
    SELECT
        m.month_start,
        SUM(s.monthly_price) AS starting_mrr
    FROM months m
    JOIN subscriptions s
        ON DATE(s.start_date) <= DATE(m.month_start)
        AND (s.end_date IS NULL OR DATE(s.end_date) >= DATE(m.month_start))
    GROUP BY m.month_start
),
churned_mrr AS (
    SELECT
        m.month_start,
        SUM(s.monthly_price) AS churned_mrr
    FROM months m
    JOIN subscriptions s
        ON DATE(s.end_date) >= DATE(m.month_start)
        AND DATE(s.end_date) < DATE(m.month_start, '+1 month')
    GROUP BY m.month_start
)
SELECT
    sm.month_start,
    sm.starting_mrr,
    COALESCE(cm.churned_mrr, 0) AS churned_mrr,
    ROUND(COALESCE(cm.churned_mrr, 0) * 1.0 / sm.starting_mrr, 3) AS revenue_churn_rate
FROM starting_mrr sm
LEFT JOIN churned_mrr cm USING(month_start)
ORDER BY month_start;
"""

print("Running Revenue Churn SQL…\n")
df = pd.read_sql_query(query, engine)
print(df)

df.to_csv("revenue_churn.csv", index=False)
print("\nSaved revenue_churn.csv")
