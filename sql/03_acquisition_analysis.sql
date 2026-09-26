-- ==============================================================================
-- 03_acquisition_analysis.sql
-- Acquisition Analysis: Volume vs Quality Framework
--
-- CRITICAL INSIGHT:
-- Channels must be evaluated by downstream user quality and revenue contribution,
-- not solely top-of-funnel acquisition volume.
--
-- DATA QUALITY NOTE:
-- The '(data deleted)' category displays 8.00% conversion and $7.67 rev/user, but
-- is a privacy-masked/redacted tracking artifact and is excluded from strategic
-- channel recommendations.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Traffic Source Performance & Volume vs. Quality Classification
-- ------------------------------------------------------------------------------
SELECT
    traffic_source,
    COUNT(user_pseudo_id) AS total_users,
    ROUND(100.0 * COUNT(user_pseudo_id) / 270154.0, 2) AS pct_total_traffic,
    SUM(viewed_item) AS viewers,
    ROUND(100.0 * SUM(viewed_item) / COUNT(user_pseudo_id), 2) AS view_rate_pct,
    SUM(added_to_cart) AS carters,
    ROUND(100.0 * SUM(CASE WHEN viewed_item=1 AND added_to_cart=1 THEN 1 ELSE 0 END) / NULLIF(SUM(viewed_item), 0), 2) AS cart_overlap_pct,
    SUM(began_checkout) AS checkouts,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS overall_purchase_conv_pct,
    SUM(total_revenue) AS total_revenue,
    ROUND(SUM(total_revenue) / COUNT(user_pseudo_id), 2) AS revenue_per_user,
    ROUND(SUM(total_revenue) / NULLIF(SUM(purchased), 0), 2) AS revenue_per_purchaser_all,
    CASE 
        WHEN traffic_source = '(data deleted)' THEN 'Redacted / Tracking Artifact (Exclude from Strategy)'
        WHEN COUNT(user_pseudo_id) >= 63462 AND (100.0 * SUM(purchased) / COUNT(user_pseudo_id)) >= 1.50 THEN 'High Volume / High Quality'
        WHEN COUNT(user_pseudo_id) >= 63462 THEN 'High Volume / Low Quality'
        WHEN (100.0 * SUM(purchased) / COUNT(user_pseudo_id)) >= 1.50 THEN 'Low Volume / High Quality'
        ELSE 'Low Volume / Low Quality'
    END AS channel_classification
FROM user_funnel
GROUP BY traffic_source
ORDER BY total_users DESC;

-- ------------------------------------------------------------------------------
-- 2. Traffic Medium Performance
-- ------------------------------------------------------------------------------
SELECT
    traffic_medium,
    COUNT(user_pseudo_id) AS total_users,
    ROUND(100.0 * COUNT(user_pseudo_id) / 270154.0, 2) AS pct_total_traffic,
    SUM(viewed_item) AS viewers,
    SUM(purchased) AS purchasers,
    ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 2) AS purchase_conv_pct,
    SUM(total_revenue) AS total_revenue,
    ROUND(SUM(total_revenue) / COUNT(user_pseudo_id), 2) AS revenue_per_user,
    CASE 
        WHEN traffic_medium = '(data deleted)' THEN 'Redacted / Tracking Artifact'
        ELSE 'Standard Medium'
    END AS medium_note
FROM user_funnel
GROUP BY traffic_medium
ORDER BY total_users DESC;
