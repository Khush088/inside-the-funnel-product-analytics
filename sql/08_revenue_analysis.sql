-- ==============================================================================
-- 08_revenue_analysis.sql
-- Revenue Analysis & Purchaser Monetization Distribution
--
-- DATA QUALITY HANDLING:
-- Total Purchasers = 4,419.
-- Positive-Revenue Purchasers = 4,066.
-- Zero-Revenue Purchasers = 353.
-- These 353 records are retained in the funnel as purchasers (based on the purchased flag)
-- but explicitly handled in revenue and monetization calculations.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. High-Level Revenue Summary Metrics
-- ------------------------------------------------------------------------------
WITH summary_stats AS (
    SELECT
        COUNT(*) AS total_users,
        SUM(purchased) AS total_purchasers,
        SUM(CASE WHEN purchased = 1 AND total_revenue > 0 THEN 1 ELSE 0 END) AS positive_purchasers,
        SUM(CASE WHEN purchased = 1 AND total_revenue = 0 THEN 1 ELSE 0 END) AS zero_rev_purchasers,
        SUM(total_revenue) AS total_revenue,
        MAX(total_revenue) AS max_user_revenue
    FROM user_funnel
)
SELECT
    total_revenue,
    total_purchasers,
    positive_purchasers,
    zero_rev_purchasers,
    ROUND(1.0 * total_revenue / total_users, 2) AS revenue_per_user_all,
    ROUND(1.0 * total_revenue / total_purchasers, 2) AS revenue_per_purchaser_all,
    ROUND(1.0 * total_revenue / positive_purchasers, 2) AS revenue_per_positive_purchaser,
    max_user_revenue
FROM summary_stats;

-- ------------------------------------------------------------------------------
-- 2. Revenue by Behavioral Segment
-- ------------------------------------------------------------------------------
SELECT
    CASE 
        WHEN purchased = 1 THEN 'Purchaser'
        WHEN began_checkout = 1 THEN 'Checkout Abandoner'
        WHEN added_to_cart = 1 THEN 'Cart Abandoner'
        WHEN viewed_item = 1 THEN 'Browser'
        ELSE 'No Engagement'
    END AS behavioral_segment,
    COUNT(user_pseudo_id) AS users,
    ROUND(100.0 * COUNT(user_pseudo_id) / 270154.0, 2) AS pct_of_user_base,
    SUM(total_revenue) AS total_revenue,
    ROUND(100.0 * SUM(total_revenue) / 362165.0, 2) AS pct_of_total_revenue,
    ROUND(SUM(total_revenue) / COUNT(user_pseudo_id), 2) AS revenue_per_user
FROM user_funnel
GROUP BY 1
ORDER BY total_revenue DESC;

-- ------------------------------------------------------------------------------
-- 3. Top-Tier Purchaser Concentration (Pareto Distribution)
-- ------------------------------------------------------------------------------
WITH ranked_purchasers AS (
    SELECT
        user_pseudo_id,
        total_revenue,
        NTILE(10) OVER (ORDER BY total_revenue DESC) AS decile
    FROM user_funnel
    WHERE purchased = 1 AND total_revenue > 0
)
SELECT
    decile,
    COUNT(*) AS purchasers_in_decile,
    SUM(total_revenue) AS decile_revenue,
    ROUND(100.0 * SUM(total_revenue) / 362165.0, 2) AS pct_of_total_revenue
FROM ranked_purchasers
GROUP BY decile
ORDER BY decile ASC;
