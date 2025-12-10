import pandas as pd
from sqlalchemy import create_engine

DB_PATH = r"C:\Users\DELL\OneDrive\Desktop\Project\saas-kpis\saas_kpis.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

query = """
WITH base AS (
    SELECT 
        s.customer_id,
        s.monthly_price,
        s.start_date,
        s.end_date,
        c.plan
    FROM subscriptions s
    JOIN customers c USING(customer_id)
),

-- Active customers per plan
active AS (
    SELECT 
        plan,
        COUNT(*) AS active_customers,
        SUM(monthly_price) AS total_mrr
    FROM base
    WHERE end_date IS NULL
    GROUP BY plan
),

-- Churned customers per plan
churn AS (
    SELECT 
        plan,
        COUNT(*) AS churned_customers
    FROM base
    WHERE end_date IS NOT NULL
    GROUP BY plan
)

SELECT
    a.plan,
    a.active_customers,
    COALESCE(c.churned_customers, 0) AS churned_customers,

    ROUND(a.total_mrr * 1.0 / a.active_customers, 2) AS ARPU,

    ROUND(COALESCE(c.churned_customers, 0) * 1.0 / a.active_customers, 3) AS churn_rate,

    CASE 
        WHEN COALESCE(c.churned_customers, 0) = 0 THEN NULL
        ELSE ROUND((a.total_mrr * 1.0 / a.active_customers) / (COALESCE(c.churned_customers, 0) * 1.0 / a.active_customers), 2)
    END AS LTV
FROM active a
LEFT JOIN churn c USING(plan)
ORDER BY plan;
"""

print("\nRunning Segmented LTV Analysis...\n")
df = pd.read_sql_query(query, engine)
print(df)

df.to_csv("segment_ltv.csv", index=False)
print("\nSaved: segment_ltv.csv")
