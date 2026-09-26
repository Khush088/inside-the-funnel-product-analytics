-- 01_data_quality.sql
-- Data quality checks
-- This script checks row count, unique users, nulls, flag consistency, purchaser/revenue inconsistency, etc.
-- NOTE: The data represents user-level aggregated data. We CANNOT do event sequencing, timestamp analysis, 
-- or session-level paths. The funnel flags represent user-level stage reach, NOT chronological event sequences.

SELECT 'total_rows' AS check_name, COUNT(*) AS result FROM user_funnel
UNION ALL
SELECT 'unique_users', COUNT(DISTINCT user_pseudo_id) FROM user_funnel
UNION ALL
SELECT 'null_user_ids', SUM(CASE WHEN user_pseudo_id IS NULL THEN 1 ELSE 0 END) FROM user_funnel
UNION ALL
SELECT 'purchasers', SUM(purchased) FROM user_funnel
UNION ALL
SELECT 'zero_rev_purchasers', SUM(CASE WHEN purchased = 1 AND total_revenue = 0 THEN 1 ELSE 0 END) FROM user_funnel
UNION ALL
SELECT 'negative_revenue', SUM(CASE WHEN total_revenue < 0 THEN 1 ELSE 0 END) FROM user_funnel
UNION ALL
SELECT 'zero_session_count', SUM(CASE WHEN session_count = 0 THEN 1 ELSE 0 END) FROM user_funnel
UNION ALL
SELECT 'inconsistent_funnel_began_chk_no_cart', SUM(CASE WHEN began_checkout = 1 AND added_to_cart = 0 THEN 1 ELSE 0 END) FROM user_funnel
UNION ALL
SELECT 'inconsistent_funnel_purchased_no_chk', SUM(CASE WHEN purchased = 1 AND began_checkout = 0 THEN 1 ELSE 0 END) FROM user_funnel;
