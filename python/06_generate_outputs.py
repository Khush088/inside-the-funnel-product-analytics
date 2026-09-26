"""
06_generate_outputs.py
Generate all required analytical output CSV files according to locked Master Specification.

Reads from the cleaned dataset (or raw data) and produces:
  - funnel_analysis.csv
  - funnel_transitions.csv
  - acquisition_analysis.csv
  - device_analysis.csv
  - country_analysis.csv
  - revenue_analysis.csv
  - north_star_comparison.csv
  - opportunity_prioritization.csv
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'user_behavior_clean.csv')

os.makedirs(OUTPUT_DIR, exist_ok=True)
df = pd.read_csv(DATA_PATH)
total_users = len(df)

print(f"Loaded {total_users:,} users from cleaned dataset.")

# ============================================================
# 1. FUNNEL ANALYSIS (Stage Reach and Intersection Overlap)
# ============================================================
print("\n--- Generating funnel_analysis.csv & funnel_transitions.csv ---")

viewers = int(df['viewed_item'].sum())
carters = int(df['added_to_cart'].sum())
checkouters = int(df['began_checkout'].sum())
purchasers = int(df['purchased'].sum())

# Overall Stage Reach (Marginal Totals)
funnel = pd.DataFrame({
    'stage': ['All Users', 'Product View', 'Add to Cart', 'Begin Checkout', 'Purchase'],
    'users': [total_users, viewers, carters, checkouters, purchasers],
    'pct_of_total': [
        100.0,
        round(viewers / total_users * 100, 2),
        round(carters / total_users * 100, 2),
        round(checkouters / total_users * 100, 2),
        round(purchasers / total_users * 100, 2)
    ]
})

# Correct Intersection-Based Funnel Transitions (User-Level Stage Reach and Overlap)
# Flag intersections:
view_and_cart = int(len(df[(df['viewed_item'] == 1) & (df['added_to_cart'] == 1)]))
cart_and_checkout = int(len(df[(df['added_to_cart'] == 1) & (df['began_checkout'] == 1)]))
checkout_and_purchased = int(len(df[(df['began_checkout'] == 1) & (df['purchased'] == 1)]))

transitions = pd.DataFrame({
    'transition': ['View -> Cart', 'Cart -> Checkout', 'Checkout -> Purchase'],
    'from_stage': ['Product View', 'Add to Cart', 'Begin Checkout'],
    'to_stage': ['Add to Cart', 'Begin Checkout', 'Purchase'],
    'denominator_users': [viewers, carters, checkouters],
    'intersecting_users': [view_and_cart, cart_and_checkout, checkout_and_purchased],
    'stage_progression_pct': [
        round(view_and_cart / viewers * 100, 2) if viewers else 0,
        round(cart_and_checkout / carters * 100, 2) if carters else 0,
        round(checkout_and_purchased / checkouters * 100, 2) if checkouters else 0
    ],
    'stage_dropoff_pct': [
        round((1 - view_and_cart / viewers) * 100, 2) if viewers else 0,
        round((1 - cart_and_checkout / carters) * 100, 2) if carters else 0,
        round((1 - checkout_and_purchased / checkouters) * 100, 2) if checkouters else 0
    ],
    'users_lost': [
        viewers - view_and_cart,
        carters - cart_and_checkout,
        checkouters - checkout_and_purchased
    ],
    'notes': [
        '6 users added to cart without viewed_item flag; direct intersection is 12,539',
        '4,058 users began checkout without added_to_cart flag; direct intersection is 5,657',
        'All 4,419 purchasers have began_checkout flag; direct intersection is 4,419'
    ]
})

funnel.to_csv(os.path.join(OUTPUT_DIR, 'funnel_analysis.csv'), index=False)
transitions.to_csv(os.path.join(OUTPUT_DIR, 'funnel_transitions.csv'), index=False)
print("Overall Funnel:")
print(funnel.to_string(index=False))
print("\nFunnel Transitions (Intersection Overlap):")
print(transitions[['transition', 'denominator_users', 'intersecting_users', 'stage_progression_pct', 'stage_dropoff_pct', 'users_lost']].to_string(index=False))

# ============================================================
# 2. ACQUISITION ANALYSIS
# ============================================================
print("\n--- Generating acquisition_analysis.csv ---")

acq_metrics = []
for col_name, col_label in [('traffic_source', 'Source'), ('traffic_medium', 'Medium')]:
    for val in df[col_name].unique():
        subset = df[df[col_name] == val]
        n = len(subset)
        n_viewed = subset['viewed_item'].sum()
        n_carted = subset['added_to_cart'].sum()
        n_checkout = subset['began_checkout'].sum()
        n_purchased = subset['purchased'].sum()
        rev = subset['total_revenue'].sum()
        
        # Intersections
        vc_int = len(subset[(subset['viewed_item'] == 1) & (subset['added_to_cart'] == 1)])
        cc_int = len(subset[(subset['added_to_cart'] == 1) & (subset['began_checkout'] == 1)])
        cp_int = len(subset[(subset['began_checkout'] == 1) & (subset['purchased'] == 1)])
        
        acq_metrics.append({
            'dimension': col_label,
            'value': val,
            'users': n,
            'pct_of_total_users': round(n / total_users * 100, 2),
            'viewers': n_viewed,
            'view_rate_pct': round(n_viewed / n * 100, 2) if n else 0,
            'view_to_cart_int': vc_int,
            'cart_conv_pct_of_viewers': round(vc_int / n_viewed * 100, 2) if n_viewed else 0,
            'cart_to_checkout_int': cc_int,
            'checkout_conv_pct_of_carters': round(cc_int / n_carted * 100, 2) if n_carted else 0,
            'purchasers': n_purchased,
            'purchase_conv_pct_of_checkouters': round(cp_int / n_checkout * 100, 2) if n_checkout else 0,
            'purchase_conv_pct_of_all': round(n_purchased / n * 100, 2) if n else 0,
            'total_revenue': rev,
            'revenue_per_user': round(rev / n, 2) if n else 0,
            'revenue_per_purchaser_all': round(rev / n_purchased, 2) if n_purchased else 0,
            'notes': 'Privacy-masked data-quality category; exclude from strategy' if val == '(data deleted)' else 'Standard channel'
        })

acq_df = pd.DataFrame(acq_metrics)
acq_df.to_csv(os.path.join(OUTPUT_DIR, 'acquisition_analysis.csv'), index=False)
print(f"  Saved {len(acq_df)} rows to acquisition_analysis.csv")

# ============================================================
# 3. DEVICE ANALYSIS
# ============================================================
print("\n--- Generating device_analysis.csv ---")

device_metrics = []
for device in ['desktop', 'mobile', 'tablet']:
    subset = df[df['device_category'] == device]
    n = len(subset)
    n_viewed = subset['viewed_item'].sum()
    n_carted = subset['added_to_cart'].sum()
    n_checkout = subset['began_checkout'].sum()
    n_purchased = subset['purchased'].sum()
    rev = subset['total_revenue'].sum()
    
    vc_int = len(subset[(subset['viewed_item'] == 1) & (subset['added_to_cart'] == 1)])
    cc_int = len(subset[(subset['added_to_cart'] == 1) & (subset['began_checkout'] == 1)])
    cp_int = len(subset[(subset['began_checkout'] == 1) & (subset['purchased'] == 1)])
    
    pos_purchasers = subset[(subset['purchased'] == 1) & (subset['total_revenue'] > 0)]
    
    device_metrics.append({
        'device': device,
        'users': n,
        'pct_of_total': round(n / total_users * 100, 2),
        'viewers': n_viewed,
        'view_rate_pct': round(n_viewed / n * 100, 2),
        'cart_overlap_users': vc_int,
        'cart_progression_pct_of_viewers': round(vc_int / n_viewed * 100, 2) if n_viewed else 0,
        'checkout_overlap_users': cc_int,
        'checkout_progression_pct_of_carters': round(cc_int / n_carted * 100, 2) if n_carted else 0,
        'purchasers': n_purchased,
        'purchase_progression_pct_of_checkouters': round(cp_int / n_checkout * 100, 2) if n_checkout else 0,
        'overall_purchase_conv_pct': round(n_purchased / n * 100, 2),
        'total_revenue': rev,
        'revenue_per_user': round(rev / n, 2),
        'revenue_per_purchaser_all': round(rev / n_purchased, 2) if n_purchased else 0,
        'revenue_per_positive_purchaser': round(rev / len(pos_purchasers), 2) if len(pos_purchasers) else 0,
        'statistical_note': 'Device vs purchase: Chi2=3.53, p=0.171 (not statistically significant). Mobile is a monitoring dimension, not a problem area.'
    })

device_df = pd.DataFrame(device_metrics)
device_df.to_csv(os.path.join(OUTPUT_DIR, 'device_analysis.csv'), index=False)
print(device_df[['device', 'users', 'pct_of_total', 'overall_purchase_conv_pct', 'total_revenue', 'revenue_per_user']].to_string(index=False))

# ============================================================
# 4. COUNTRY ANALYSIS (Volume filter > 500 users)
# ============================================================
print("\n--- Generating country_analysis.csv ---")

MIN_USERS = 500

country_metrics = []
for country in df['country'].unique():
    subset = df[df['country'] == country]
    n = len(subset)
    if n < MIN_USERS:
        continue
    n_viewed = subset['viewed_item'].sum()
    n_purchased = subset['purchased'].sum()
    rev = subset['total_revenue'].sum()
    pos_purch = subset[(subset['purchased'] == 1) & (subset['total_revenue'] > 0)]
    
    country_metrics.append({
        'country': country,
        'users': n,
        'pct_of_total_users': round(n / total_users * 100, 2),
        'viewers': n_viewed,
        'view_rate_pct': round(n_viewed / n * 100, 2),
        'purchasers': n_purchased,
        'purchase_conv_pct': round(n_purchased / n * 100, 2),
        'total_revenue': rev,
        'revenue_per_user': round(rev / n, 2),
        'revenue_per_purchaser_all': round(rev / n_purchased, 2) if n_purchased else 0,
        'revenue_per_positive_purchaser': round(rev / len(pos_purch), 2) if len(pos_purch) else 0
    })

country_df = pd.DataFrame(country_metrics).sort_values('users', ascending=False)

# Market Classification
median_users_c = country_df['users'].median()
median_conv_c = country_df['purchase_conv_pct'].median()
country_df['market_type'] = 'Standard'
country_df.loc[(country_df['users'] >= median_users_c) & (country_df['purchase_conv_pct'] >= median_conv_c), 'market_type'] = 'High-Volume High-Value'
country_df.loc[(country_df['users'] >= median_users_c) & (country_df['purchase_conv_pct'] < median_conv_c), 'market_type'] = 'High-Volume Opportunity'
country_df.loc[(country_df['users'] < median_users_c) & (country_df['purchase_conv_pct'] >= median_conv_c), 'market_type'] = 'High-Value Niche'
country_df.loc[(country_df['users'] < median_users_c) & (country_df['purchase_conv_pct'] < median_conv_c), 'market_type'] = 'Low-Volume Low-Value'

country_df.to_csv(os.path.join(OUTPUT_DIR, 'country_analysis.csv'), index=False)
print(f"  {len(country_df)} countries with >= {MIN_USERS} users saved.")

# ============================================================
# 5. REVENUE ANALYSIS (Addressing 353 zero-revenue purchasers)
# ============================================================
print("\n--- Generating revenue_analysis.csv ---")

total_rev = int(df['total_revenue'].sum())
purchaser_df = df[df['purchased'] == 1]
non_zero_rev_purchasers = purchaser_df[purchaser_df['total_revenue'] > 0]
zero_rev_purchasers = purchaser_df[purchaser_df['total_revenue'] == 0]

sorted_rev = non_zero_rev_purchasers['total_revenue'].sort_values(ascending=False)
top_10_pct_n = int(len(sorted_rev) * 0.1)
top_20_pct_n = int(len(sorted_rev) * 0.2)
rev_top_10 = int(sorted_rev.head(top_10_pct_n).sum())
rev_top_20 = int(sorted_rev.head(top_20_pct_n).sum())

rev_summary = pd.DataFrame([
    {'metric': 'Total Revenue', 'value': float(total_rev), 'unit': 'USD'},
    {'metric': 'Total Purchasers', 'value': float(len(purchaser_df)), 'unit': 'Users'},
    {'metric': 'Positive-Revenue Purchasers', 'value': float(len(non_zero_rev_purchasers)), 'unit': 'Users'},
    {'metric': 'Zero-Revenue Purchasers (Flagged)', 'value': float(len(zero_rev_purchasers)), 'unit': 'Users'},
    {'metric': 'Revenue per User (All Users)', 'value': round(total_rev / total_users, 2), 'unit': 'USD/User'},
    {'metric': 'Revenue per Purchaser (All 4,419 Purchasers)', 'value': round(total_rev / len(purchaser_df), 2), 'unit': 'USD/Purchaser'},
    {'metric': 'Revenue per Positive Purchaser (4,066 Purchasers)', 'value': round(total_rev / len(non_zero_rev_purchasers), 2), 'unit': 'USD/Purchaser'},
    {'metric': 'Median Revenue (Positive Purchasers)', 'value': float(non_zero_rev_purchasers['total_revenue'].median()), 'unit': 'USD'},
    {'metric': 'Mean Revenue (Positive Purchasers)', 'value': round(non_zero_rev_purchasers['total_revenue'].mean(), 2), 'unit': 'USD'},
    {'metric': 'Maximum Single-User Revenue', 'value': float(df['total_revenue'].max()), 'unit': 'USD'},
    {'metric': 'Revenue from Top 10% Purchasers', 'value': float(rev_top_10), 'unit': 'USD'},
    {'metric': 'Top 10% Purchaser Revenue Share %', 'value': round(rev_top_10 / total_rev * 100, 2), 'unit': 'Percent'},
    {'metric': 'Revenue from Top 20% Purchasers', 'value': float(rev_top_20), 'unit': 'USD'},
    {'metric': 'Top 20% Purchaser Revenue Share %', 'value': round(rev_top_20 / total_rev * 100, 2), 'unit': 'Percent'}
])

rev_summary.to_csv(os.path.join(OUTPUT_DIR, 'revenue_analysis.csv'), index=False)
print(rev_summary.to_string(index=False))

# ============================================================
# 6. NORTH STAR METRIC COMPARISON
# ============================================================
print("\n--- Generating north_star_comparison.csv ---")

ns_candidates = pd.DataFrame([
    {
        'metric_name': 'Purchase Conversion Rate',
        'current_value': '1.64%',
        'status': 'RECOMMENDED',
        'represents_customer_value': 'Yes (successful fulfillment of purchase intent)',
        'reflects_product_success': 'Yes (measures full end-to-end funnel efficiency)',
        'connects_to_business': 'Yes (directly drives customer volume and top-line scale)',
        'measurable_consistently': 'Yes (binary flag user aggregation)',
        'actionable_by_product': 'Yes (directly influenced by UX, discovery, and checkout friction)',
        'avoids_perverse_incentives': 'Yes (cannot be artificially inflated by raising prices)',
        'evaluation_score': 6,
        'strategic_justification': 'Primary North Star. Aligns full product team on moving users through the journey without distortions.'
    },
    {
        'metric_name': 'Revenue Per User',
        'current_value': '$1.34',
        'status': 'Secondary Metric',
        'represents_customer_value': 'Partial (composite monetary metric)',
        'reflects_product_success': 'Yes (balances conversion and order value)',
        'connects_to_business': 'Yes (direct financial revenue measure)',
        'measurable_consistently': 'Yes (total_revenue / total_users)',
        'actionable_by_product': 'Partial (affected by pricing and catalogue mix)',
        'avoids_perverse_incentives': 'Partial (could incentivize optimizing for high-ticket buyers at expense of buyer base)',
        'evaluation_score': 5,
        'strategic_justification': 'Strong supporting business metric, but secondary to conversion rate.'
    },
    {
        'metric_name': 'View-to-Purchase Conversion',
        'current_value': '7.21%',
        'status': 'Diagnostic Funnel Metric',
        'represents_customer_value': 'Yes (measures intent conversion)',
        'reflects_product_success': 'Yes (measures merchandising and product page effectiveness)',
        'connects_to_business': 'Yes (converts product browsers to buyers)',
        'measurable_consistently': 'Yes (purchased / viewed_item)',
        'actionable_by_product': 'Yes (highly actionable for store/catalog teams)',
        'avoids_perverse_incentives': 'Yes (focuses on intent fulfillment)',
        'evaluation_score': 5,
        'strategic_justification': 'Excellent diagnostic metric for the merchandising experience, but excludes upper-funnel landing traffic.'
    },
    {
        'metric_name': 'Purchase Count',
        'current_value': '4,419',
        'status': 'Volume Indicator',
        'represents_customer_value': 'Yes (volume of fulfilled orders)',
        'reflects_product_success': 'Partial (confounds marketing traffic acquisition with product efficiency)',
        'connects_to_business': 'Yes (scales total customer base)',
        'measurable_consistently': 'Yes (raw count of purchasers)',
        'actionable_by_product': 'Partial (heavily dependent on marketing ad spend)',
        'avoids_perverse_incentives': 'Yes',
        'evaluation_score': 4,
        'strategic_justification': 'Useful volume counter, but fails to normalize for acquisition traffic changes.'
    },
    {
        'metric_name': 'Total Revenue',
        'current_value': '$362,165',
        'status': 'Executive Business KPI',
        'represents_customer_value': 'Partial (captures financial exchange, not user friction)',
        'reflects_product_success': 'Partial (lagging indicator; can mask funnel drop-offs with high AOV)',
        'connects_to_business': 'Yes (primary financial outcome)',
        'measurable_consistently': 'Yes (sum of total_revenue)',
        'actionable_by_product': 'Partial (lagging, composite outcome)',
        'avoids_perverse_incentives': 'No (can be inflated through price increases while conversion plummets)',
        'evaluation_score': 3,
        'strategic_justification': 'Ultimate company financial KPI, but inappropriate as a product-level North Star.'
    }
])

ns_candidates.to_csv(os.path.join(OUTPUT_DIR, 'north_star_comparison.csv'), index=False)
print(ns_candidates[['metric_name', 'current_value', 'status', 'evaluation_score']].to_string(index=False))

# ============================================================
# 7. OPPORTUNITY PRIORITIZATION (RICE Framework)
# ============================================================
print("\n--- Generating opportunity_prioritization.csv ---")

opportunities = pd.DataFrame([
    {
        'priority': 1,
        'opportunity': 'View-to-Cart Conversion Improvement',
        'problem_statement': '79.53% of product viewers (48,713 users) drop off without adding an item to cart',
        'affected_users': viewers - view_and_cart,
        'reach_score': 5,
        'impact_score': 5,
        'confidence_score': 4,
        'effort_score': 3,
        'rice_score': round((5 * 5 * 4) / 3, 1),
        'recommended_intervention': 'Implement prominent sticky Add-to-Cart CTAs, product page trust badges, stock urgency, and clear pricing',
        'primary_metric': 'View-to-Cart Conversion Rate',
        'strategic_rationale': 'Highest-leverage product opportunity. Affects 61,252 high-intent viewers where 48,713 drop off before cart.',
        'methodological_note': 'RICE impact, confidence, and effort scores are analyst-assessed directional estimates, not experimentally measured values.'
    },
    {
        'priority': 2,
        'opportunity': 'Checkout-to-Purchase Conversion',
        'problem_statement': '54.51% of users who begin checkout (5,296 users) drop off before completing purchase',
        'affected_users': checkouters - checkout_and_purchased,
        'reach_score': 3,
        'impact_score': 4,
        'confidence_score': 4,
        'effort_score': 3,
        'rice_score': round((3 * 4 * 4) / 3, 1),
        'recommended_intervention': 'Streamline guest checkout, expand express payment methods (Google Pay, PayPal), display transparent shipping upfront',
        'primary_metric': 'Checkout-to-Purchase Conversion Rate',
        'strategic_rationale': 'High-intent bottleneck at final transaction hurdle. Converting checkout abandoners provides immediate revenue yield.',
        'methodological_note': 'RICE scores are directional analyst estimates.'
    },
    {
        'priority': 3,
        'opportunity': 'Cart-to-Checkout Friction Reduction',
        'problem_statement': '54.91% of cart users (6,888 users) drop off without beginning checkout',
        'affected_users': carters - cart_and_checkout,
        'reach_score': 2,
        'impact_score': 3,
        'confidence_score': 3,
        'effort_score': 2,
        'rice_score': round((2 * 3 * 3) / 2, 1),
        'recommended_intervention': 'Add slide-in mini-cart drawer with instant Proceed to Checkout CTA and free shipping progress bars',
        'primary_metric': 'Cart-to-Checkout Conversion Rate',
        'strategic_rationale': 'Secondary friction point where 6,888 carters abandon before checkout; actionable via instant mini-cart drawer and threshold indicators.',
        'methodological_note': 'RICE scores are directional analyst estimates.'
    },
    {
        'priority': 4,
        'opportunity': 'Non-Viewer Activation & Landing Page Relevance',
        'problem_statement': '77.33% of users (208,902 users) never view a product page after landing on site',
        'affected_users': total_users - viewers,
        'reach_score': 5,
        'impact_score': 2,
        'confidence_score': 2,
        'effort_score': 4,
        'rice_score': round((5 * 2 * 2) / 4, 1),
        'recommended_intervention': 'Optimize homepage hero merchandising, category navigation hierarchy, and personalized popular product recommendations',
        'primary_metric': 'Product View Rate',
        'strategic_rationale': 'Massive user volume, but low confidence whether non-viewing is product friction or low-intent bounced acquisition traffic.',
        'methodological_note': 'RICE scores are directional analyst estimates.'
    }
])

opportunities.to_csv(os.path.join(OUTPUT_DIR, 'opportunity_prioritization.csv'), index=False)
print(opportunities[['priority', 'opportunity', 'affected_users', 'rice_score']].to_string(index=False))

print("\n=== ALL OUTPUTS SUCCESSFULLY REGENERATED ===")
