WITH months AS (
    SELECT DATE('2024-01-01') AS month_start UNION ALL
    SELECT DATE('2024-02-01') UNION ALL
    SELECT DATE('2024-03-01') UNION ALL
    SELECT DATE('2024-04-01') UNION ALL
    SELECT DATE('2024-05-01') UNION ALL
    SELECT DATE('2024-06-01')
)
SELECT
    m.month_start,
    SUM(s.monthly_price) AS mrr
FROM months m
JOIN subscriptions s
    ON DATE(s.start_date) <= DATE(m.month_start, '+1 month', '-1 day')
    AND (s.end_date IS NULL OR DATE(s.end_date) >= DATE(m.month_start))
GROUP BY m.month_start
ORDER BY m.month_start;
