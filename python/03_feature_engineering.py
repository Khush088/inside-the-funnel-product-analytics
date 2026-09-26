import pandas as pd
import numpy as np
import os

def main():
    print("Running Feature Engineering...")
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    df = pd.read_csv('data/raw/ga4_user_level_funnel.csv')
    
    # engagement_level
    def get_engagement(row):
        if row['active_days'] == 1 and row['session_count'] <= 1:
            return 'Low'
        elif row['active_days'] <= 3 and row['session_count'] <= 3:
            return 'Medium'
        else:
            return 'High'
    df['engagement_level'] = df.apply(get_engagement, axis=1)
    
    # funnel_stage_reached
    def get_funnel_stage(row):
        if row['purchased'] == 1: return 'purchased'
        if row['began_checkout'] == 1: return 'checkout'
        if row['added_to_cart'] == 1: return 'carted'
        if row['viewed_item'] == 1: return 'viewed'
        return 'none'
    df['funnel_stage_reached'] = df.apply(get_funnel_stage, axis=1)
    
    # is_zero_revenue_purchaser
    df['is_zero_revenue_purchaser'] = ((df['purchased'] == 1) & (df['total_revenue'] == 0)).astype(int)
    
    # user_segment
    def get_segment(row):
        if row['purchased'] == 1:
            return 'Purchaser'
        elif row['began_checkout'] == 1:
            return 'Checkout Abandoner'
        elif row['added_to_cart'] == 1:
            return 'Cart Abandoner'
        elif row['viewed_item'] == 1:
            return 'Browser'
        else:
            return 'No Engagement'
    df['user_segment'] = df.apply(get_segment, axis=1)
    
    # revenue_per_session
    df['revenue_per_session'] = np.where(df['session_count'] > 0, df['total_revenue'] / df['session_count'], 0)
    
    df.to_csv('data/processed/user_behavior_clean.csv', index=False)
    
    segment_summary = df['user_segment'].value_counts().reset_index()
    segment_summary.columns = ['Segment', 'Count']
    segment_summary.to_csv('outputs/behavioral_segments.csv', index=False)
    
    print("Features engineered. Data saved.")

if __name__ == "__main__":
    main()
