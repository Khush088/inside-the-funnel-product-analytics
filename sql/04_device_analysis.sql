-- ==============================================================================
-- 04_device_analysis.sql
-- Device Category Performance Analysis
--
-- STATISTICAL CONCLUSION:
-- Chi-square test: Chi2 = 3.533658, p-value = 0.170874, Cramer's V = 0.002383.
-- There is NO statistically significant association between device category and purchase.
-- Purchase conversion is broadly similar across devices (Mobile: 1.69%, Desktop: 1.60%, Tablet: 1.57%).
-- Mobile is treated as an ongoing monitoring dimension, NOT a prioritized problem area.
-- ==============================================================================

SELECT
    device_category,
    COUNT(user_pseudo_id) AS total_users,
    ROUND(100.0 * COUNT(user_pseudo_id) / 270154.0, 2) AS pct_of_total_users,
    SUM(viewed_item) AS viewers,
    ROUND(100.0 * SUM(viewed_item) / COUNT(user_pseudo_id), 2) AS view_rate_pct,
    -- Stage Overlaps
    SUM(CASE WHEN viewed_item=1 AND added_to_cart=1 THEN 1 ELSE 0 END) AS view_and_cart_users,
    ROUND(100.0 * SUM(CASE WHEN viewed_item=1 AND added_to_cart=1 THEN 1 ELSE 0 END) / NULLIF(SUM(viewed_item), 0), 2) AS cart_progression_pct_of_viewers,
    SUM(CASE WHEN added_to_cart=1 AND began_checkout=1 THEN 1 ELSE 0 END) AS cart_and_checkout_users,
    ROUND(100.0 * SUM(CASE WHEN added_to_cart=1 AND began_checkout=1 THEN 1 ELSE 0 END) / NULLIF(SUM(added_to_cart), 0), 2) AS checkout_progression_pct_of_carters,
    SUM(CASE WHEN began_checkout=1 AND purchased=1 THEN 1 ELSE 0 END) AS checkout_and_purchased_users,
    ROUND(100.0 * SUM(CASE WHEN began_checkout=1 AND purchased=1 THEN 1 ELSE 0 END) / NULLIF(SUM(began_checkout), 0), 2) AS purchase_progression_pct_of_checkouts,
    SUM(purchased) AS total_purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS overall_purchase_conv_pct,
    SUM(total_revenue) AS total_revenue,
    ROUND(SUM(total_revenue) / COUNT(user_pseudo_id), 2) AS revenue_per_user,
    ROUND(SUM(total_revenue) / NULLIF(SUM(purchased), 0), 2) AS revenue_per_purchaser_all,
    ROUND(SUM(total_revenue) / NULLIF(SUM(CASE WHEN purchased = 1 AND total_revenue > 0 THEN 1 ELSE 0 END), 0), 2) AS revenue_per_positive_purchaser
FROM user_funnel
WHERE device_category IN ('desktop', 'mobile', 'tablet')
GROUP BY device_category
ORDER BY total_users DESC;
