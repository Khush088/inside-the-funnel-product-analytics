-- ==============================================================================
-- 02_funnel_analysis.sql
-- Inside the Funnel: Diagnosing Drop-off and Driving Conversion (Google Merchandise Store)
--
-- CRITICAL METHODOLOGICAL NOTE:
-- The data represents user-level aggregated data, NOT timestamped clickstream events.
-- Funnel metrics therefore represent user-level stage reach and intersection overlap,
-- NOT chronological sequential event transitions.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- PART 1: Overall User-Level Stage Reach (Marginal Totals)
-- ------------------------------------------------------------------------------
WITH overall_stage_reach AS (
    SELECT
        COUNT(*) AS total_users,
        SUM(viewed_item) AS viewed_item_users,
        SUM(added_to_cart) AS added_to_cart_users,
        SUM(began_checkout) AS began_checkout_users,
        SUM(purchased) AS purchased_users
    FROM user_funnel
)
SELECT 
    'Stage Reach' AS metric_type,
    total_users,
    viewed_item_users,
    ROUND(100.0 * viewed_item_users / total_users, 2) AS pct_viewed_of_total,
    added_to_cart_users,
    ROUND(100.0 * added_to_cart_users / total_users, 2) AS pct_carted_of_total,
    began_checkout_users,
    ROUND(100.0 * began_checkout_users / total_users, 2) AS pct_checkout_of_total,
    purchased_users,
    ROUND(100.0 * purchased_users / total_users, 2) AS pct_purchased_of_total
FROM overall_stage_reach;

-- ------------------------------------------------------------------------------
-- PART 2: Stage Overlap & Progression Rates (Intersection Logic)
-- ------------------------------------------------------------------------------
-- Because stage flags are not strictly nested in GA4 user-level aggregations:
-- - View -> Cart: Intersection is 12,539 users (6 users added to cart without viewed_item)
-- - Cart -> Checkout: Intersection is 5,657 users (4,058 began checkout without added_to_cart)
-- - Checkout -> Purchase: Intersection is 4,419 users (0 purchased without began_checkout)
-- ------------------------------------------------------------------------------
WITH stage_intersections AS (
    SELECT
        COUNT(*) AS total_users,
        SUM(viewed_item) AS viewers,
        SUM(added_to_cart) AS carters,
        SUM(began_checkout) AS checkouts,
        SUM(purchased) AS purchasers,
        -- Exact intersections
        SUM(CASE WHEN viewed_item = 1 AND added_to_cart = 1 THEN 1 ELSE 0 END) AS view_and_cart_users,
        SUM(CASE WHEN added_to_cart = 1 AND began_checkout = 1 THEN 1 ELSE 0 END) AS cart_and_checkout_users,
        SUM(CASE WHEN began_checkout = 1 AND purchased = 1 THEN 1 ELSE 0 END) AS checkout_and_purchased_users
    FROM user_funnel
)
SELECT
    'View -> Cart' AS transition,
    viewers AS denominator_users,
    view_and_cart_users AS intersecting_users,
    ROUND(100.0 * view_and_cart_users / NULLIF(viewers, 0), 2) AS progression_rate_pct,
    ROUND(100.0 * (1.0 - 1.0 * view_and_cart_users / NULLIF(viewers, 0)), 2) AS dropoff_rate_pct,
    (viewers - view_and_cart_users) AS users_lost,
    'Primary bottleneck: 79.53% drop-off among viewers' AS strategic_note
FROM stage_intersections
UNION ALL
SELECT
    'Cart -> Checkout' AS transition,
    carters AS denominator_users,
    cart_and_checkout_users AS intersecting_users,
    ROUND(100.0 * cart_and_checkout_users / NULLIF(carters, 0), 2) AS progression_rate_pct,
    ROUND(100.0 * (1.0 - 1.0 * cart_and_checkout_users / NULLIF(carters, 0)), 2) AS dropoff_rate_pct,
    (carters - cart_and_checkout_users) AS users_lost,
    '45.09% overlap progression; 6,888 cart abandoners' AS strategic_note
FROM stage_intersections
UNION ALL
SELECT
    'Checkout -> Purchase' AS transition,
    checkouts AS denominator_users,
    checkout_and_purchased_users AS intersecting_users,
    ROUND(100.0 * checkout_and_purchased_users / NULLIF(checkouts, 0), 2) AS progression_rate_pct,
    ROUND(100.0 * (1.0 - 1.0 * checkout_and_purchased_users / NULLIF(checkouts, 0)), 2) AS dropoff_rate_pct,
    (checkouts - checkout_and_purchased_users) AS users_lost,
    '45.49% progression; 5,296 checkout abandoners' AS strategic_note
FROM stage_intersections;
