-- 06_behavior_analysis.sql
-- Behavioral analysis using active_days and session_count
-- NOTE: The data represents user-level aggregated data. We CANNOT do event sequencing, timestamp analysis, 
-- or session-level paths. The funnel flags represent user-level stage reach, NOT chronological event sequences.

WITH engagement_buckets AS (
    SELECT
        user_pseudo_id,
        purchased,
        total_revenue,
        session_count,
        active_days,
        CASE
            WHEN active_days = 1 AND session_count <= 1 THEN 'Low'
            WHEN active_days <= 3 AND session_count <= 3 THEN 'Medium'
            ELSE 'High'
        END AS engagement_level
    FROM user_funnel
)
-- By bucket
SELECT
    engagement_level,
    COUNT(user_pseudo_id) AS total_users,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS purchase_rate_pct,
    AVG(total_revenue) AS avg_revenue,
    AVG(session_count) AS avg_sessions
FROM engagement_buckets
GROUP BY engagement_level
ORDER BY 
    CASE engagement_level 
        WHEN 'High' THEN 1 
        WHEN 'Medium' THEN 2 
        WHEN 'Low' THEN 3 
    END;

-- Cross-tab: active_days x purchased
SELECT
    active_days,
    COUNT(user_pseudo_id) AS total_users,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS purchase_rate_pct
FROM user_funnel
GROUP BY active_days
ORDER BY active_days;

-- Cross-tab: session_count x purchased
SELECT
    session_count,
    COUNT(user_pseudo_id) AS total_users,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS purchase_rate_pct
FROM user_funnel
GROUP BY session_count
ORDER BY session_count;
