-- ==============================================================================
-- 09_north_star_metrics.sql
-- North Star Metric Evaluation & Strategic Recommendation
--
-- SELECTION CRITERIA:
-- 1. Represents customer value (fulfilling purchase intent)
-- 2. Reflects product success (full funnel efficiency)
-- 3. Connects to business outcomes (revenue growth)
-- 4. Measurable consistently (reliable user aggregation)
-- 5. Actionable by product teams (responsive to UX/friction reductions)
-- 6. Avoids perverse incentives (cannot be gamed by inflating prices)
-- ==============================================================================

WITH metrics AS (
    SELECT
        SUM(purchased) AS purchase_count,
        ROUND(100.0 * SUM(purchased) / COUNT(user_pseudo_id), 4) AS purchase_conversion_rate,
        SUM(total_revenue) AS total_revenue,
        ROUND(SUM(total_revenue) / COUNT(user_pseudo_id), 4) AS revenue_per_user,
        ROUND(100.0 * SUM(CASE WHEN viewed_item = 1 AND purchased = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(viewed_item), 0), 4) AS view_to_purchase_conversion
    FROM user_funnel
)
SELECT
    'Purchase Conversion Rate' AS candidate_metric,
    CAST(purchase_conversion_rate AS STRING) || '%' AS current_value,
    'RECOMMENDED NORTH STAR' AS selection_status,
    6 AS evaluation_score,
    'Reflects complete funnel health normalized for traffic volume. Highly actionable and resistant to pricing distortions.' AS rationale
FROM metrics
UNION ALL
SELECT
    'Revenue Per User',
    '$' || CAST(revenue_per_user AS STRING),
    'Secondary Outcome Metric',
    5,
    'Balances conversion and order value, directly linked to business revenue, but may incentivize high-ticket skew.'
FROM metrics
UNION ALL
SELECT
    'View-to-Purchase Conversion',
    CAST(view_to_purchase_conversion AS STRING) || '%' AS current_value,
    'Diagnostic Funnel Metric',
    5,
    'Measures intentional product exploration efficiency, though excludes upper-funnel landing traffic.'
FROM metrics
UNION ALL
SELECT
    'Purchase Count',
    CAST(purchase_count AS STRING),
    'Volume Tracking Metric',
    4,
    'Direct volume count, but fails to normalize for marketing acquisition traffic swings.'
FROM metrics
UNION ALL
SELECT
    'Total Revenue',
    '$' || CAST(total_revenue AS STRING),
    'Executive Business KPI',
    3,
    'Crucial financial lagging metric, but poor product North Star because it can mask conversion drops with price hikes.'
FROM metrics
ORDER BY evaluation_score DESC;
