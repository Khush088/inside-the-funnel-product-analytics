-- 07_user_segmentation.sql
-- Create behavioral segments
-- NOTE: The data represents user-level aggregated data. We CANNOT do event sequencing, timestamp analysis, 
-- or session-level paths. The funnel flags represent user-level stage reach, NOT chronological event sequences.

WITH segments AS (
    SELECT
        user_pseudo_id,
        active_days,
        session_count,
        total_revenue,
        CASE
            WHEN purchased = 1 THEN 'Purchaser'
            WHEN began_checkout = 1 AND purchased = 0 THEN 'Checkout Abandoner'
            WHEN added_to_cart = 1 AND began_checkout = 0 AND purchased = 0 THEN 'Cart Abandoner'
            WHEN viewed_item = 1 AND added_to_cart = 0 AND began_checkout = 0 AND purchased = 0 THEN 'Browser'
            WHEN viewed_item = 0 AND added_to_cart = 0 AND began_checkout = 0 AND purchased = 0 THEN 'No Engagement'
            ELSE 'Other'
        END AS user_segment
    FROM user_funnel
),
totals AS (
    SELECT COUNT(*) as all_users FROM segments
)
SELECT
    s.user_segment,
    COUNT(s.user_pseudo_id) AS total_users,
    ROUND(100.0 * COUNT(s.user_pseudo_id) / MAX(t.all_users), 2) AS percent_of_total,
    AVG(s.active_days) AS avg_active_days,
    AVG(s.session_count) AS avg_session_count,
    SUM(s.total_revenue) AS total_revenue,
    SUM(s.total_revenue) / COUNT(s.user_pseudo_id) AS revenue_per_user
FROM segments s
CROSS JOIN totals t
GROUP BY s.user_segment
ORDER BY total_users DESC;
