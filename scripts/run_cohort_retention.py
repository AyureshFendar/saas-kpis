import pandas as pd
from sqlalchemy import create_engine

DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

query = """
WITH cohort AS (
    SELECT
        customer_id,
        STRFTIME('%Y-%m', start_date) AS cohort_month,
        start_date,
        end_date
    FROM subscriptions
),

all_months AS (
    SELECT DATE('2024-01-01') AS month_start UNION ALL
    SELECT DATE('2024-02-01') UNION ALL
    SELECT DATE('2024-03-01') UNION ALL
    SELECT DATE('2024-04-01') UNION ALL
    SELECT DATE('2024-05-01') UNION ALL
    SELECT DATE('2024-06-01')
),

activity AS (
    SELECT
        c.cohort_month,
        m.month_start,
        COUNT(*) AS active_users
    FROM cohort c
    JOIN all_months m
        ON DATE(c.start_date) <= DATE(m.month_start)
       AND (c.end_date IS NULL OR DATE(c.end_date) >= DATE(m.month_start))
    GROUP BY c.cohort_month, m.month_start
),

cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(*) AS cohort_size
    FROM cohort
    GROUP BY cohort_month
)

SELECT
    a.cohort_month,
    STRFTIME('%Y-%m', a.month_start) AS active_month,
    ROUND(a.active_users * 1.0 / cs.cohort_size, 3) AS retention_rate
FROM activity a
JOIN cohort_sizes cs USING(cohort_month)
ORDER BY cohort_month, active_month;
"""

print("\nRunning Corrected Cohort Retention SQL...\n")
df = pd.read_sql_query(query, engine)
print(df)

df.to_csv("cohort_retention.csv", index=False)
print("\nSaved corrected cohort_retention.csv!")
