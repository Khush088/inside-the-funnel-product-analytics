-- ==============================================================================
-- 10_opportunity_prioritization.sql
-- RICE Framework Opportunity Prioritization (Reach, Impact, Confidence, Effort)
--
-- METHODOLOGICAL NOTE:
-- RICE impact, confidence, and effort scores are analyst-assessed directional estimates,
-- not experimentally measured values.
--
-- DEVICE NOTE:
-- Device category showed no statistically significant association with purchase
-- (Chi2 = 3.53, p = 0.171), so mobile is treated as an ongoing monitoring dimension
-- rather than a prioritized strategic intervention.
-- ==============================================================================

SELECT
    1 AS priority,
    'Opportunity 1: View-to-Cart Conversion Improvement' AS opportunity,
    48713 AS affected_users,
    5 AS reach,       -- Affects 61,252 product viewers (48,713 drop off before cart)
    5 AS impact,      -- Largest single conditional drop-off in user funnel (79.53%)
    4 AS confidence,  -- Highly reliable behavioral data showing massive drop-off
    3 AS effort,      -- Product page redesign, sticky CTAs, social proof
    ROUND((5 * 5 * 4) / 3.0, 1) AS rice_score,
    'Highest-priority product opportunity based on observed funnel drop-off and directional RICE score' AS strategic_status
UNION ALL
SELECT
    2,
    'Opportunity 2: Checkout-to-Purchase Conversion',
    5296,
    3 AS reach,       -- Affects 9,715 checkout starters (5,296 drop off)
    4 AS impact,      -- High-intent bottom-of-funnel users
    4 AS confidence,  -- High certainty on checkout drop-off volume
    3 AS effort,      -- Guest checkout, payment options, transparent fees
    ROUND((3 * 4 * 4) / 3.0, 1) AS rice_score,
    'High-priority monetization opportunity addressing bottom-funnel friction'
UNION ALL
SELECT
    3,
    'Opportunity 3: Cart-to-Checkout Friction Reduction',
    6888,
    2 AS reach,       -- Affects 12,545 carters (6,888 cart abandoners)
    3 AS impact,      -- High-intent carters dropping before checkout
    3 AS confidence,  -- Observable cart abandonment
    2 AS effort,      -- Mini-cart drawer, free shipping threshold bar
    ROUND((2 * 3 * 3) / 2.0, 1) AS rice_score,
    'Medium-priority refinement to streamline cart transition'
UNION ALL
SELECT
    4,
    'Opportunity 4: Non-Viewer Activation & Landing Page Relevance',
    208902,
    5 AS reach,       -- Affects 208,902 users who never view a product
    2 AS impact,      -- Many may be low-intent bounced acquisition traffic
    2 AS confidence,  -- Difficult to separate product friction from traffic quality
    4 AS effort,      -- Homepage redesign, marketing audience realignment
    ROUND((5 * 2 * 2) / 4.0, 1) AS rice_score,
    'Exploratory/growth opportunity requiring coordination with marketing'
ORDER BY priority ASC;
