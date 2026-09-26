-- 05_country_analysis.sql
-- Country-level analysis
-- NOTE: The data represents user-level aggregated data. We CANNOT do event sequencing, timestamp analysis, 
-- or session-level paths. The funnel flags represent user-level stage reach, NOT chronological event sequences.

-- Top 15 by volume
SELECT
    country,
    COUNT(user_pseudo_id) AS total_users,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS purchase_conv_pct,
    SUM(total_revenue) AS total_revenue,
    SUM(total_revenue) / COUNT(user_pseudo_id) AS revenue_per_user
FROM user_funnel
GROUP BY country
HAVING COUNT(user_pseudo_id) >= 500
ORDER BY total_users DESC
LIMIT 15;

-- Top 15 by conversion (with 500 user threshold)
SELECT
    country,
    COUNT(user_pseudo_id) AS total_users,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS purchase_conv_pct,
    SUM(total_revenue) AS total_revenue,
    SUM(total_revenue) / COUNT(user_pseudo_id) AS revenue_per_user
FROM user_funnel
GROUP BY country
HAVING COUNT(user_pseudo_id) >= 500
ORDER BY purchase_conv_pct DESC
LIMIT 15;

-- Top 15 by revenue (with 500 user threshold)
SELECT
    country,
    COUNT(user_pseudo_id) AS total_users,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS purchase_conv_pct,
    SUM(total_revenue) AS total_revenue,
    SUM(total_revenue) / COUNT(user_pseudo_id) AS revenue_per_user
FROM user_funnel
GROUP BY country
HAVING COUNT(user_pseudo_id) >= 500
ORDER BY total_revenue DESC
LIMIT 15;
